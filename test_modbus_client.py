"""
Test Modbus TCP Client to read holding registers from a Modbus Server.
This script connects to a Modbus Server, reads holding registers, and prints the values.
Make sure to update the SERVER_IP, PORT, and UNIT_ID variables to match your Modbus"""
from pymodbus.client import ModbusTcpClient
import logging

# Optional: Enable logging to see the raw packets being sent/received
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# --- Configuration ---
SERVER_IP = "192.168.0.90"  # Change to your Modbus Server IP
PORT = 5020  # Default Modbus TCP port
UNIT_ID = 1  # Also known as Slave ID


def run_modbus_client():
    """Run the Modbus TCP client to read holding registers."""
    # 1. Initialize the client
    client = ModbusTcpClient(SERVER_IP, port=PORT)

    try:
        # 2. Establish connection
        connection = client.connect()
        if not connection:
            logging.error("Unable to connect to %s:%s", SERVER_IP, PORT)
            return

        logging.info("Connected successfully!")

        # 3. Read Holding Registers
        # address: The starting register address (0-indexed)
        # count: Number of registers to read
        # slave: The Unit ID
        response = client.read_holding_registers(address=1, count=1)

        # 4. Handle Response
        if not response.isError():
            logging.info("Register Values: %s", response.registers)
        else:
            logging.error("Error reading registers: %s", response)

    except Exception as e:
        logging.error("An error occurred: %s", e)

    finally:
        # 5. Always close the connection
        client.close()
        logging.info("Connection closed.")


if __name__ == "__main__":
    run_modbus_client()
