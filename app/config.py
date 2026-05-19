"""
Configuration file for the Modbus application.
Defines constants for MQTT, Modbus, and logging settings."""
import os

MQTT_BROKER = os.getenv(
    "MQTT_BROKER",
    "192.168.0.90"
)

MQTT_PORT = int(
    os.getenv(
        "MQTT_PORT",
        1883
    )
)

TOPIC_SUBSCRIBE = "device/modbus/in"
TOPIC_PUBLISH = "device/modbus/out"

# Modbus
MODBUS_HOST = "0.0.0.0"
MODBUS_PORT = 5020

# logs
LOG_DIR = "logs"
LOG_FILE = "modbus_app.log"
APP_NAME = "ModbusApplication"
