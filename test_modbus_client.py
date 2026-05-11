from pymodbus.client import ModbusTcpClient
import logging

# Optional: Enable logging to see the raw packets being sent/received
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# --- Configuration ---
SERVER_IP = '192.168.0.90'  # Change to your Modbus Server IP
PORT = 5020               # Default Modbus TCP port
UNIT_ID = 1              # Also known as Slave ID

def run_modbus_client():
    # 1. Initialize the client
    client = ModbusTcpClient(SERVER_IP, port=PORT)

    try:
        # 2. Establish connection
        connection = client.connect()
        if not connection:
            print(f"Unable to connect to {SERVER_IP}:{PORT}")
            return

        print("Connected successfully!")

        # 3. Read Holding Registers
        # address: The starting register address (0-indexed)
        # count: Number of registers to read
        # slave: The Unit ID
        response = client.read_holding_registers(address=1, count=1)

        # 4. Handle Response
        if not response.isError():
            print(f"Register Values: {response.registers}")
        else:
            print(f"Error reading registers: {response}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # 5. Always close the connection
        client.close()
        print("Connection closed.")

if __name__ == "__main__":
    run_modbus_client()