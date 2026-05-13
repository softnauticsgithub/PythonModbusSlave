import logging
from config import APP_NAME
from helper import write_u32

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)

async def parseMessage(message = None, datastore = None):
    """
    Parses a message and extracts relevant information.
    Args:
        message (str): The message to be parsed.
        datastore: The datastore to update with parsed values.
    """
    logger.debug(f"Parsing message: {message}")
    if message:
        # Process the message
        event_type = message.get("event",{}).get("type")
        if event_type == "update":
            logger.info(f"Received telemetry update: {message}")
            timestamp = message.get("timestamp")
            logger.debug(f"Event Received at timestamp: {timestamp}")
            logger.debug(f"Message Originated from: {message.get('origin').get('service')}")
            logger.debug(f"Message Routed from: {message.get('source').get('service')}")
            payloads = message.get("payload",[])
            for item in payloads:
                update_register(
                    item,
                    datastore
                )
        else:
            logger.warning(f"Received unsupported event type: {event_type}, Message: {message}")
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
    logger.debug(f"Attempting to find mapping for key={key} in register map")
    for address, parameter in modbus_mappping.items():
        if parameter.get("name") == key:
            reg_info = parameter
            logger.debug(f"Found mapping for key={key}")
            break

    if not reg_info:
        logger.debug(
            f"[WARN] "
            f"No mapping for key={key}"
        )
        return

    address = reg_info.get("address")
    length = reg_info.get("length", 1)

    if length > 1:
        reg1, reg2 = write_u32(value)
        datastore.setValuesfromCentral(
            address,
            [reg1, reg2]
        )
        logger.debug(
            f"[MODBUS] "
            f"{key}={value} "
            f"-> [{address},{address+1}]"
        )
    else:
        datastore.setValuesfromCentral(
            address,
            [value]
        )
        logger.debug(
            f"[MODBUS] "
            f"{key}={value} "
            f"-> [{address}]"
        )