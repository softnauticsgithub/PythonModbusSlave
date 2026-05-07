from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from EventBus import EventBus
from customDatastore import ConfigurableDataBlock
from modbusRegisters import RegisterMap
from mqttEventHandler import MQTTManager
from zmqEventHandler import ZMQAdapter
from config import MODBUS_HOST, MODBUS_PORT

# Initialize register map and initial values
map_obj = RegisterMap()
map_obj.setRegisters()

# Create EventBus
event_bus = EventBus()

# Register adapters
zmq_adapter = ZMQAdapter()
mqtt_obj = MQTTManager()


event_bus.register(zmq_adapter)

data_block = ConfigurableDataBlock(0, map_obj.register_initial_values, map_obj.register_map, event_callback=mqtt_obj)
mqtt_obj.attach_datastore(data_block)

store = ModbusSlaveContext(
    hr=data_block
)

context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName = "EVStatePoC"
identity.ProductCode = "EVCS"
identity.ProductName = "Charging_Controller"
identity.MajorMinorRevision = "1.0"

print(f"Starting Modbus TCP Server on port {MODBUS_PORT}...")
StartTcpServer(context, identity=identity, address=(MODBUS_HOST, MODBUS_PORT))