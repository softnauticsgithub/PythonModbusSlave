from pymodbus.datastore import ModbusSequentialDataBlock
from customExceptions import IllegalAddress

class ConfigurableDataBlock(ModbusSequentialDataBlock):

    def __init__(self, address, values, reg_map, event_callback=None):
        super().__init__(address, values)
        self.reg_map = reg_map
        self.event_callback = event_callback

    
    def validate(self, address, count=1):
        for i in range(count):
            reg_addr = address + i
            reg_info = self.reg_map.get(reg_addr)

            if not reg_info:
                raise IllegalAddress(f"Invalid address: {reg_addr}")

            if reg_info.get("access") == "r":
                raise IllegalAddress(f"Read-only register: {reg_addr}")

        return True

    def setValues(self, address, values):
        for i, val in enumerate(values):
            reg_addr = address + i
            reg_info = self.reg_map.get(reg_addr)

            if reg_info:
                access = reg_info.get("access", "rw")

                if access == "r":
                    raise Exception(f"Register {reg_addr} is READ-ONLY")

        super().setValues(address, values)
        # TODO: Publish event with address and new values
        if self.event_callback: 
            self.event_callback.publish("modbus/register_update", {"address": address, "values": values})

    def getValues(self, address, count=1):
        for i in range(count):
            reg_addr = address + i
            reg_info = self.reg_map.get(reg_addr)

            if reg_info:
                access = reg_info.get("access", "rw")

                if access == "w":
                    raise Exception(f"Register {reg_addr} is WRITE-ONLY")

        return super().getValues(address, count)
    