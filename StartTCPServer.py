import asyncio
import logging
from multiprocessing.util import LOGGER_NAME
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from EventBus import EventBus
from customDatastore import ConfigurableDataBlock
from modbusRegisters import RegisterMap
from mqttEventHandler import AsyncMQTTClient
from config import MODBUS_HOST, MODBUS_PORT
from customLogger import setup_logger
from pymodbus.server import StartAsyncTcpServer

logger = setup_logger()


def configure_datablock():
    """
    Function to configure the Modbus data block with the register mapping and initial values.
    """
    map_obj = RegisterMap()
    map_obj.setRegisters()
    event_bus = EventBus()
    data_block = ConfigurableDataBlock(0, map_obj.register_initial_values, map_obj.register_map, event_callback=event_bus)
    store = ModbusSlaveContext(
        hr=data_block,
        zero_mode=True
    )
    return data_block, store, event_bus   

def register_mqtt_handler(event_bus, data_block=None):
    """
    Function to initialize and start the MQTT handler.
    """
    mqtt_obj = AsyncMQTTClient(datastore=data_block)
    event_bus.register(mqtt_obj)
    return mqtt_obj, event_bus


async def start_modbus_server(store):
    """
    Main function to set up and start the Modbus TCP server with MQTT integration.
    """

    #3. Start Modbus TCP Server
    context = ModbusServerContext(slaves=store, single=True)
    identity = ModbusDeviceIdentification()
    identity.VendorName = "EVStatePoC"
    identity.ProductCode = "EVCS"
    identity.ProductName = "Charging_Controller"
    identity.MajorMinorRevision = "1.0"
    logger.info("Activate the Modbus Subscriber to see the MQTT events being published based on Modbus register changes...")
    logger.info(f"Starting Modbus TCP Server on port {MODBUS_PORT}...")
    
    #4. Start the Modbus TCP server
    await StartAsyncTcpServer(context=context, identity=identity, address=(MODBUS_HOST, MODBUS_PORT))

async def main():
    """
    Main entry point to start the Modbus TCP server and MQTT handler.
    """
    # 1. Initialize the data block and register map
    data_block, store, event_bus = configure_datablock()

    #1. MQTT Handler
    mqtt_obj, event_bus = register_mqtt_handler(event_bus, data_block)

    mqtt_task = asyncio.create_task(
        mqtt_obj.start()
    )

    modbus_task = asyncio.create_task(
        start_modbus_server(store)
    )

    tasks = [
        mqtt_task,
        modbus_task
    ]

    try:
        #5. Run the Modbus TCP server and MQTT handler concurrently
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        logger.error("[MAIN] Cancelled")
    finally:
        for task in tasks:
            task.cancel()
        await asyncio.gather(
            *tasks,
            return_exceptions=True
        )

if __name__ == "__main__":
    asyncio.run(main())