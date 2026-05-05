class EventBus:
    def __init__(self):
        self.adapters = []

    def register(self, adapter):
        self.adapters.append(adapter)

    def publish(self, event: dict):
        for adapter in self.adapters:
            adapter.publish(event)