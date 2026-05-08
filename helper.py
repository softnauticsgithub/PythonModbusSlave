import struct

def write_u32(value):
    packed = struct.pack(">I", value)
    regs = struct.unpack(">HH", packed)
    return regs

def read_u32(regs):
    packed = struct.pack(">HH", *regs)
    return struct.unpack(">I", packed)[0]

#TODO: Need to add Support for Float values across multiple registers as well (e.g. 32-bit float across two 16-bit registers)