import asyncio
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from EventBus import EventBus
from customDatastore import ConfigurableDataBlock
from modbusRegisters import RegisterMap
from mqttEventHandler import AsyncMQTTClient
from config import MODBUS_HOST, MODBUS_PORT
from pymodbus.server import StartAsyncTcpServer

def register_mapping():
    """
    Function to define the register mapping and initial values for the Modbus server."""
    # Define register mapping and initial values
    # Initialize register map and initial values
    map_obj = RegisterMap()
    map_obj.setRegisters()
    return map_obj

def register_mqtt_handler():
    """
    Function to initialize and start the MQTT handler.
    """
    # Create EventBus
    event_bus = EventBus()
    mqtt_obj = AsyncMQTTClient()
    event_bus.register(mqtt_obj)
    return mqtt_obj, event_bus

def configure_datastore(mqtt_obj, event_bus):
    """
    Function to configure the Modbus datastore with the register mapping and MQTT event handling.
    """
    map_obj = register_mapping()
    data_block = ConfigurableDataBlock(0, map_obj.register_initial_values, map_obj.register_map, event_callback=event_bus)
    mqtt_obj.attach_datastore(data_block)
    store = ModbusSlaveContext(
        hr=data_block,
        zero_mode=True
    )
    return store


async def start_modbus_server(mqtt_obj, event_bus):
    """
    Main function to set up and start the Modbus TCP server with MQTT integration.
    """

    #2. Configure Modbus Datastore with MQTT event handling
    store = configure_datastore(mqtt_obj, event_bus)
    
    #3. Start Modbus TCP Server
    context = ModbusServerContext(slaves=store, single=True)
    identity = ModbusDeviceIdentification()
    identity.VendorName = "EVStatePoC"
    identity.ProductCode = "EVCS"
    identity.ProductName = "Charging_Controller"
    identity.MajorMinorRevision = "1.0"
    print("Activate the Modbus Subscriber to see the MQTT events being published based on Modbus register changes...")
    print(f"Starting Modbus TCP Server on port {MODBUS_PORT}...")
    
    #4. Start the Modbus TCP server
    await StartAsyncTcpServer(context=context, identity=identity, address=(MODBUS_HOST, MODBUS_PORT))

async def main():
    """
    Main entry point to start the Modbus TCP server and MQTT handler."""
    #1. MQTT Handler
    mqtt_obj, event_bus = register_mqtt_handler()

    #5. Run the Modbus TCP server and MQTT handler concurrently
    asyncio.gather(
        start_modbus_server(mqtt_obj, event_bus),
        mqtt_obj.start()
    )

if __name__ == "__main__":
    asyncio.run(main())