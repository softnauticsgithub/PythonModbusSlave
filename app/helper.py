"""
Helper functions for handling multi-register values in Modbus communication.
This module provides utility functions to write and read 32-bit unsigned integer values across two 16-bit Modbus registers, following the Big-Endian format commonly used in Modbus implementations.
"""

import struct


def write_u32(value):
    """
    Helper function to write a 32-bit unsigned integer value across two 16-bit Modbus registers.
    :param value: The 32-bit unsigned integer value to be written.
    :return: A tuple containing the two 16-bit register values.
    """
    packed = struct.pack(">I", value)
    regs = struct.unpack(">HH", packed)
    return regs


def read_u32(regs):
    """
    Helper function to read a 32-bit unsigned integer value from two 16-bit Modbus registers.
    :param regs: A tuple containing the two 16-bit register values.
    :return: The 32-bit unsigned integer value.
    """
    packed = struct.pack(">HH", *regs)
    return struct.unpack(">I", packed)[0]


# TODO: Need to add Support for Float values across multiple registers as well (e.g. 32-bit float across two 16-bit registers)
