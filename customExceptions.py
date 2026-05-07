from pymodbus.exceptions import ModbusException
from pymodbus.constants import ExceptionCodes

class IllegalFunction(ModbusException):
    code = ExceptionCodes.IllegalFunction

class IllegalAddress(ModbusException):
    code = ExceptionCodes.IllegalAddress
    

class IllegalValue(ModbusException):
    code = ExceptionCodes.IllegalValue

class DeviceFailure(ModbusException):
    code = ExceptionCodes.SlaveFailure