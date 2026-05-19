"""
Custom exceptions for Modbus operations.
"""
from pymodbus.exceptions import ModbusException


class IllegalFunction(ModbusException):
    """
    Exception raised when an illegal function code is received.
    """


class IllegalAddress(ModbusException):
    """
    Exception raised when an illegal data address is received.
    """


class IllegalValue(ModbusException):
    """
    Exception raised when an illegal value is received.
    """


class DeviceFailure(ModbusException):
    """
    Exception raised when a device failure occurs.
    """
