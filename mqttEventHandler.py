import json
import asyncio
import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT, TOPIC_SUBSCRIBE, TOPIC_PUBLISH

class AsyncMQTTClient:

    def __init__(
        self,
        broker=MQTT_BROKER,
        port=MQTT_PORT,
        client_id="modbus_service",
        subscribe_topic=TOPIC_SUBSCRIBE,
        publish_topic=TOPIC_PUBLISH
    ):
        """
        Async MQTT Client to handle communication with central engine.
        :param broker: MQTT broker address
        :param port: MQTT broker port
        :param client_id: Unique identifier for the MQTT client
        :param subscribe_topic: Topic to subscribe to
        :param publish_topic: Topic to publish to
        """
        self.datastore = None
        self.broker = broker
        self.port = port
        self.subscribe_topic = subscribe_topic
        self.publish_topic = publish_topic

        # Async loop
        self.loop = asyncio.get_running_loop()

        # Queue bridge
        self.message_queue = asyncio.Queue()

        # MQTT client
        self.client = mqtt.Client(
            client_id=client_id
        )
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.running = False


    def attach_datastore(self, datastore):
        self.datastore = datastore

    def _on_connect(
        self,
        client,
        userdata,
        flags,
        rc
    ):
        """
        Callback for MQTT connection event.
        """
        print(f"[MQTT] Connected: {rc}")
        client.subscribe(
            self.subscribe_topic
        )
        print(
            f"[MQTT SUB] "
            f"{self.subscribe_topic}"
        )

    def _on_message(
        self,
        client,
        userdata,
        msg
    ):
        """
        Callback for MQTT message event.
        """
        
        try:
            topic = msg.topic
            payload = json.loads(
                msg.payload.decode()
            )
            print(
                f"[MQTT RX] "
                f"{topic} -> {payload}"
            )

            # Push into asyncio queue
            asyncio.run_coroutine_threadsafe(

                self.message_queue.put(
                    (topic, payload)
                ),
                self.loop
            )
        except json.JSONDecodeError as e:
            print(f"[INVALID JSON] {e}")
        except Exception as e:
            print(f"[MQTT ERROR] {e}")

    async def start(self):
        """
        Start the MQTT client and processing loop.
        """
        self.running = True
        self.client.connect(
            self.broker,
            self.port,
            60
        )
        # Start paho internal thread
        self.client.loop_start()
        print("[MQTT] Loop Started")
        # Start processing messages
        await self._message_loop()

    async def _message_loop(self):
        """
        Async loop to process incoming MQTT messages from the queue.
        """
        try:
            while self.running:
                topic, payload = await self.message_queue.get()
                await self.handle_message(
                    topic,
                    payload
                )
        except asyncio.CancelledError:
            print("[MQTT] Message loop cancelled")

    async def handle_message(
        self,
        topic,
        payload
    ):
        """
        Messages received from central engine
        """
        print(
            f"[ENGINE -> DEVICE] {topic} -> {payload}"
        )
        if self.datastore:
            address = int(payload.get("address"))
            value = int(payload.get("value"))
            print(f"Updating address {address} with value {value}")
            self.datastore.setValuesfromCentral(
                address,
                [value]
            )
        #TODO: Implement command handling logic based on payload content
        # For example, you can check for specific commands and perform actions accordingly


    async def publish(
        self,
        payload
    ):
        """
        Publish messages to central engine.
        :param payload: Dictionary representing the message payload
        """
        if isinstance(payload, dict):
            payload = json.dumps(payload)

        self.client.publish(
            self.publish_topic,
            payload
        )

        print(
            f"[MQTT PUB] "
            f"{self.publish_topic} -> "
            f"{payload}"
        )

    async def stop(self):
        self.running = False
        self.client.loop_stop()
        self.client.disconnect()
        print("[MQTT] Stopped")