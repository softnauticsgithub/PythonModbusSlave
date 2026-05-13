import yaml
from helper import write_u32, read_u32
import logging

logger = logging.getLogger(__name__)

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
            self.register_map[addr] = reg

        # Build ordered register list
        max_addr = max(self.register_map.keys())
        self.register_initial_values = [0] * (max_addr + 1)

        # TODO: Optimize this logic by adding type in yaml file for more standard way
        for index, reg_info in self.register_map.items():
            default = reg_info.get("default", 0)
            length = reg_info.get("length", 1)
            if length > 1:
                self.register_initial_values[index:index + length] = write_u32(default)
            else:
                self.register_initial_values[index] = default
        logger.info(f"Register Map: {self.register_map}")
        logger.info(f"Initial Values: {self.register_initial_values}")
