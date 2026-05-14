"""
Module for parsing messages received from the central engine and updating the Modbus registers accordingly.
"""
import logging
from config import APP_NAME
from helper import write_u32

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)

async def parseMessage(message=None, datastore=None):
    """
    Parses a message and extracts relevant information.
    Args:
        message (str): The message to be parsed.
        datastore: The datastore to update with parsed values.
    """
    logger.debug("Parsing message: %s", message)
    if message:
        # Process the message
        event_type = message.get("event", {}).get("type")
        if event_type == "update":
            logger.info("Received telemetry update: %s", message)
            timestamp = message.get("timestamp")
            logger.debug("Event Received at timestamp: %s", timestamp)
            logger.debug("Message Originated from: %s", message.get('origin').get('service'))
            logger.debug("Message Routed from: %s", message.get('source').get('service'))
            payloads = message.get("payload", [])
            for item in payloads:
                update_register(item, datastore)
        else:
            logger.warning("Received unsupported event type: %s, Message: %s", event_type, message)
        return
    else:
        logger.error("Received empty message payload")
        return


def update_register(payload, datastore):
    """
    Updates the Modbus register based on the provided payload.
    Args:
        payload (dict): The payload containing the key and value to update.
        datastore: The datastore to update with the new values.
    """
    key = payload.get("key")
    value = payload.get("value")
    modbus_mappping = datastore.reg_map
    reg_info = None
    logger.debug("Attempting to find mapping for key=%s in register map", key)
    for address, parameter in modbus_mappping.items():
        if parameter.get("name") == key:
            reg_info = parameter
            logger.debug("Found mapping for key=%s", key)
            break

    if not reg_info:
        logger.warning("[WARN] No mapping for key=%s", key)
        return

    address = reg_info.get("address")
    length = reg_info.get("length", 1)

    if length > 1:
        reg1, reg2 = write_u32(value)
        datastore.setValuesfromCentralengine(address, [reg1, reg2])
        logger.debug("[MODBUS] %s=%s -> [%s,%s]", key, value, address, address + 1)
    else:
        datastore.setValuesfromCentralengine(address, [value])
        logger.debug("[MODBUS] %s=%s -> [%s]", key, value, address)
