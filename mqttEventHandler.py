import paho.mqtt.client as mqtt
import json

class MQTTPublisher:
    def __init__(self, broker="broker.hivemq.com", port=1883):
        self.client = mqtt.Client()
        self.client.connect(broker, port)
        self.client.loop_start()

    def publish(self, topic, payload):
        message = json.dumps(payload)
        self.client.publish(topic, message)
        print(f"[MQTT] Published to {topic}: {message}")