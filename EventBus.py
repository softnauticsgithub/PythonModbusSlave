class EventBus:
    def __init__(self):
        """
        Class representing an event bus to manage and publish events to registered adapters.
        """
        self.adapters = []

    def register(self, adapter):
        """
        Method to register an adapter to the event bus.
        :param adapter: An instance of an adapter that implements a publish method.
        """
        self.adapters.append(adapter)



    async def publish(self, event: dict):
        """
        Method to publish an event to all registered adapters.
        :param event: A dictionary representing the event to be published.
        """
        for adapter in self.adapters:
            await adapter.publish(event)
