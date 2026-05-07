import json
import paho.mqtt.client as mqtt

from config import (
    MQTT_BROKER,
    MQTT_PORT,
    TOPIC_SUBSCRIBE,
    TOPIC_PUBLISH
)

class MQTTManager:

    def __init__(self):
        self.client = mqtt.Client()
        self.datastore = None
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def attach_datastore(self, datastore):
        self.datastore = datastore

    def on_connect(self, client, userdata, flags, rc):
        print(f"[MQTT] Connected: {rc}")
        client.subscribe(TOPIC_SUBSCRIBE)

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            address = int(payload["address"])
            value = int(payload["value"])

            print(f"[MQTT] Incoming Write: {address} = {value}")

            if self.datastore:
                self.datastore.setValuesfromCentral(
                    address,
                    value
                )
        except Exception as e:
            print("[MQTT ERROR]", e)

    def publish(self, payload):
        self.client.publish(
            TOPIC_PUBLISH,
            json.dumps(payload)
        )
        print(f"[MQTT] Published: {payload}")

    def start(self):

        self.client.connect(
            MQTT_BROKER,
            MQTT_PORT,
            60
        )

        self.client.loop_start()