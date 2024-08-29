# home_monitoring/broker.py
from .models import SensorData, DeviceAction, SensorState

class MessageBroker:
    _instance = None

    @staticmethod
    def get_instance():
        if MessageBroker._instance is None:
            MessageBroker()
        return MessageBroker._instance

    def __init__(self):
        if MessageBroker._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.subscribers = {}
            MessageBroker._instance = self

    def subscribe(self, topic, subscriber):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(subscriber)

    def publish(self, topic, message):
        if topic in self.subscribers:
            SensorData.log(topic, message)
            SensorState.update(topic, message)
            for subscriber in self.subscribers[topic]:
                if topic in ['humidity', 'temperature']:
                    from .sensors import Sprinkler  # Import here to avoid circular dependency
                    if isinstance(subscriber, Sprinkler):
                        if topic == 'humidity':
                            subscriber.update(humidity=message)
                        elif topic == 'temperature':
                            subscriber.update(temperature=message)
                else:
                    subscriber.update(message)
