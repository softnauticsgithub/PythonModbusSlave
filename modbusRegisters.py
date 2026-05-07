import yaml

with open("registerInfo.yml", "r") as f:
    config = yaml.safe_load(f)

registers = config["registers"]
reg_map = {}         # address → metadata
initial_values = []


class RegisterMap():

    def __init__(self):
        """
        Read Registers from YML file
        """
        with open("registerInfo.yml", "r") as f:
            config = yaml.safe_load(f)
        self.registers = config["registers"]
        self.register_map = {}         # address → metadata
        self.register_initial_values = []
    
    def setRegisters(self):
        """
        Convert YML file register info into compatible modbus block 
        """
        for reg in self.registers:
            addr = reg["address"]
            length = reg.get("length", 1)
            end_addr = addr + length - 1
            for index in range(addr, end_addr + 1): 
                self.register_map[index] = reg

        # Build ordered register list
        max_addr = max(self.register_map.keys())

        for index in range(max_addr + 1):
            if index in self.register_map:
                self.register_initial_values.append(self.register_map[index].get("default", 0))
            else:
                self.register_initial_values.append(0)
