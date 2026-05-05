from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from EventBus import EventBus
from customDatastore import ConfigurableDataBlock
from modbusRegisters import RegisterMap
from mqttEventHandler import MQTTPublisher
from zmqEventHandler import ZMQAdapter

# Initialize register map and initial values
map_obj = RegisterMap()
map_obj.setRegisters()

# Create EventBus
event_bus = EventBus()

# Register adapters
zmq_adapter = ZMQAdapter()
mqtt_obj = MQTTPublisher()


event_bus.register(zmq_adapter)




store = ModbusSlaveContext(
    hr=ConfigurableDataBlock(
        0,
        map_obj.register_initial_values,
        map_obj.register_map,
        event_callback=mqtt_obj
    )
)

context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName = "EVStatePoC"
identity.ProductCode = "EVCS"
identity.ProductName = "Charging_Controller"
identity.MajorMinorRevision = "1.0"

print("Starting Modbus TCP Server on port 5020...")
StartTcpServer(context, identity=identity, address=("0.0.0.0", 5020))