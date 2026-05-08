from pymodbus.exceptions import ModbusException

class IllegalFunction(ModbusException):
    pass

class IllegalAddress(ModbusException):
    pass

class IllegalValue(ModbusException):
    pass

class DeviceFailure(ModbusException):
    pass