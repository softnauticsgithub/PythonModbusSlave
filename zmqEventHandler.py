import zmq
import json
import time

class ZMQAdapter:
    def __init__(self, bind_addr="tcp://*:5556", topic="modbus.events"):
        self.ctx = zmq.Context.instance()
        self.sock = self.ctx.socket(zmq.PUB)
        self.sock.bind(bind_addr)
        self.topic = topic

        time.sleep(0.5)  # avoid slow joiner issue

    def publish(self, event: dict):
        payload = json.dumps(event)
        self.sock.send_multipart([
            self.topic.encode(),
            payload.encode()
        ])