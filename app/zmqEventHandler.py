"""
ZMQ Adapter for publishing Modbus events to a central engine.
This module defines a ZMQAdapter class that can be used to publish events to a central engine
"""
import zmq
import json
import time


class ZMQAdapter:
    """
    ZMQ Adapter for publishing Modbus events to a central engine.
    """
    def __init__(self, bind_addr="tcp://*:5556", topic="modbus.events"):
        """
        Initializes the ZMQ Adapter.
        :param bind_addr: The address to bind the ZMQ socket to (default: "tcp://*:5556")
        :param topic: The topic to publish events on (default: "modbus.events")
        """
        self.ctx = zmq.Context.instance()
        self.sock = self.ctx.socket(zmq.PUB)
        self.sock.bind(bind_addr)
        self.topic = topic

        time.sleep(0.5)  # avoid slow joiner issue

    def publish(self, event: dict):
        """
        Publishes an event to the central engine.
        :param event: The event to publish (as a dictionary)
        """
        payload = json.dumps(event)
        self.sock.send_multipart([self.topic.encode(), payload.encode()])
