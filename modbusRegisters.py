"""
Modbus register management module.
This module provides functionality for managing Modbus registers, including initialization and value handling.
"""

import yaml
from helper import write_u32
from config import APP_NAME
import logging

logger = logging.getLogger(APP_NAME)


with open("registerInfo.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

registers = config["registers"]
reg_map = {}  # address → metadata
initial_values = []


class RegisterMap:
    """
    Manages Modbus register mapping and initialization from YAML configuration.
    
    Provides functionality to convert register information from YML file into compatible
    modbus blocks with proper address mapping and initial values.
    """

    def __init__(self):
        """
        Read Registers from YML file
        """
        with open("registerInfo.yml", "r", encoding="utf-8") as yaml_file:
            yaml_config = yaml.safe_load(yaml_file)
        self.registers = yaml_config["registers"]
        self.register_map = {}  # address → metadata
        self.register_initial_values = []

    def set_registers(self):
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
                self.register_initial_values[index : index + length] = write_u32(default)
            else:
                self.register_initial_values[index] = default
        logger.info("Register Map: %s", self.register_map)
        logger.info("Initial Values: %s", self.register_initial_values)
