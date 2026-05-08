from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from EventBus import EventBus
from customDatastore import ConfigurableDataBlock
from modbusRegisters import RegisterMap
from mqttEventHandler import MQTTManager
from config import MODBUS_HOST, MODBUS_PORT

# Initialize register map and initial values
map_obj = RegisterMap()
map_obj.setRegisters()

# Create EventBus
event_bus = EventBus()

# Register adapters
# TODO for now support with MQTT, can add more adapters like ZMQ in future
#zmq_adapter = ZMQAdapter()
mqtt_obj = MQTTManager()
mqtt_obj.start()
event_bus.register(mqtt_obj)

data_block = ConfigurableDataBlock(0, map_obj.register_initial_values, map_obj.register_map, event_callback=event_bus)
mqtt_obj.attach_datastore(data_block)

store = ModbusSlaveContext(
    hr=data_block,
    zero_mode=True
)

context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName = "EVStatePoC"
identity.ProductCode = "EVCS"
identity.ProductName = "Charging_Controller"
identity.MajorMinorRevision = "1.0"

print(f"Starting Modbus TCP Server on port {MODBUS_PORT}...")

StartTcpServer(context=context, identity=identity, address=(MODBUS_HOST, MODBUS_PORT))