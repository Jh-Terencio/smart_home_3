from .models import SensorData, SensorState

class MessageBroker:
    _instance = None  # armazenar a única instancia do singleton

    @staticmethod
    def get_instance():
        if MessageBroker._instance is None:
            MessageBroker()  # cria 1 nova instancia se ainda n tiver uma
        return MessageBroker._instance

    def __init__(self):
        # garante que apenas 1 instancia seja criada
        if MessageBroker._instance is not None:
            raise Exception("Essa classe é um Singleton.")
        else:
            self.subscribers = {}  # dicionario p armazenar os subscribers por topico
            MessageBroker._instance = self 

    def subscribe(self, topic, subscriber):
        # add um subscriber a um topico específico
        if topic not in self.subscribers:
            self.subscribers[topic] = []  # cria uma lista de subscribers se o tópico n existir
        self.subscribers[topic].append(subscriber)

    def publish(self, topic, message):
        # publicar uma msg p todos os subscribers de um topico
        if topic in self.subscribers:
            # loga e atualiza o estado do sensor antes de notificar os subscribers
            SensorData.log(topic, message)
            SensorState.update(topic, message)
            for subscriber in self.subscribers[topic]:
                subscriber.update(message)  # notificar cada subscriber com a msg
