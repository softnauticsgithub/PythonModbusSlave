from pymodbus.datastore import ModbusSequentialDataBlock
from customExceptions import IllegalAddress

# Follow Big-Endian format for multi-register values (e.g. 32-bit values across two 16-bit registers) to be consistent with common Modbus conventions and ensure compatibility with a wide range of Modbus clients and tools that expect this format. This means that the higher-order register will contain the most significant bits of the value, while the lower-order register will contain the least significant bits. For example, if we have a 32-bit value that we want to store across two registers, the first register (lower address) will hold the lower 16 bits of the value, and the second register (higher address) will hold the upper 16 bits of the value. This approach allows for easier integration with existing Modbus systems and ensures that our implementation adheres to widely accepted standards in the Modbus community.
class ConfigurableDataBlock(ModbusSequentialDataBlock):

    def __init__(self, address, values, reg_map, event_callback=None):
        super().__init__(address, values)
        self.reg_map = reg_map
        self.event_callback = event_callback

    
    def validate(self, address, count=1):
        for i in range(count):
            reg_addr = address + i
            reg_info = self.reg_map.get(reg_addr)

        return True

    def setValues(self, address, values):
        if not isinstance(values, list):
            values = [values]

        # TODO: Handle multi-register writes and reads (e.g. writing a 32-bit value across two 16-bit registers)
        for i, val in enumerate(values):
            reg_addr = address + i
            reg_info = self.reg_map.get(reg_addr)

            if reg_info:
                access = reg_info.get("access", "rw")

                if access == "r":
                    #TODO: Program should not   crash if invalid write is attempted. Instead, it should log the error and ignore the write. 
                    raise IllegalAddress(f"Register {reg_addr} is READ-ONLY")

        super().setValues(address, values)
        # TODO: Publish event with address and new values
        if self.event_callback: 
            self.event_callback.publish({"address": address, "values": values})


    def setValuesfromCentral(self, address, values):
        # TODO: Implement pending logic to handle incoming updates from central system (e.g. via MQTT) and update the datastore accordingly. This may involve validating the incoming address and value, checking access permissions, and then updating the register values without triggering another event publication (to avoid infinite loops).
        super().setValues(address, values)

    def getValues(self, address, count=1):
        for i in range(count):
            reg_addr = address + i
            reg_info = self.reg_map.get(reg_addr)
            if reg_info:
                access = reg_info.get("access", "rw")
                if access == "w":
                    raise IllegalAddress(f"Register {reg_addr} is WRITE-ONLY")
        return super().getValues(address, count)
    