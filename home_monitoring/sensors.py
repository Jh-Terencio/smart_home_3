# home_monitoring/sensors.py

import random
from .broker import MessageBroker
from .models import DeviceAction

# Classe base para os sensores que utilizam o padrao Proxy para publicacao de dados
class SensorProxy:
    def __init__(self, broker):
        self.broker = broker
        self.last_published_values = {}

    def publish_data(self, topic, data, threshold=0.1):
        last_value = self.last_published_values.get(topic)
        if last_value is None or abs(data - last_value) > threshold:
            self.broker.publish(topic, data)
            self.last_published_values[topic] = data

# Classes especificas de sensores que herdam de SensorProxy

class TemperatureSensor(SensorProxy):
    def read_temperature(self):
        temperature = round(random.uniform(15.0, 35.0), 2)
        self.publish_data('temperature', temperature, threshold=0.5)

class HumiditySensor(SensorProxy):
    def read_humidity(self):
        humidity = round(random.uniform(20.0, 80.0), 2)
        self.publish_data('humidity', humidity, threshold=1.0)

class MotionSensor(SensorProxy):
    def detect_motion(self):
        motion_detected = random.choice([0, 1])
        self.publish_data('motion', motion_detected, threshold=0.1)

class GasSensor(SensorProxy):
    def detect_gas(self):
        gas_level = round(random.uniform(100, 500), 2)
        self.publish_data('gas', gas_level, threshold=10.0)

class LightSensor(SensorProxy):
    def read_light(self):
        light_level = round(random.uniform(0, 800), 2)
        self.publish_data('light', light_level, threshold=20.0)

# Classe base para dispositivos que atuam como Subscribers no padrao Observer

class Subscriber:
    def update(self, message):
        raise NotImplementedError("Subscribers must implement the update method.")

# Classes especificas de dispositivos que herdam de Subscriber

class SmartThermostat(Subscriber):
    def __init__(self, broker):
        self.broker = broker

    def update(self, temperature):
        """
        Atualiza o estado do termostato com base na temperatura recebida.
        Liga o ar condicionado se estiver quente ou o aquecedor se estiver frio.
        """
        acao = "A temperatura esta confortavel."
        if temperature > 25:
            acao = "Ligando o ar condicionado..."
        elif temperature < 15:
            acao = "Ligando o aquecedor..."
        print(acao)
        DeviceAction.log('Termostato Inteligente', acao, temperature)

class Humidifier(Subscriber):
    def __init__(self, broker):
        self.broker = broker

    def update(self, humidity):
        """
        Atualiza o estado do umidificador com base na umidade recebida.
        Liga o umidificador se a umidade estiver baixa.
        """
        acao = "A umidade esta em um nivel bom."
        if humidity < 40:
            acao = "Ligando o umidificador..."
        print(acao)
        DeviceAction.log('Umidificador', acao, humidity)

class SecurityAlarm(Subscriber):
    def __init__(self, broker):
        self.broker = broker

    def update(self, motion_detected):
        """
        Atualiza o estado do alarme de seguranca com base na deteccao de movimento.
        Dispara o alarme se houver movimento detectado.
        """
        acao = "Nenhum movimento detectado."
        if motion_detected:
            acao = "Movimento detectado! Disparando alarme..."
        print(acao)
        DeviceAction.log('Alarme de Seguranca', acao, motion_detected)

class GasDetector(Subscriber):
    def __init__(self, broker):
        self.broker = broker

    def update(self, gas_level):
        """
        Atualiza o estado do detector de gas com base no nivel de gas recebido.
        Aciona a ventilacao se o nivel de gas estiver elevado.
        """
        acao = "Nivel de gas normal."
        if gas_level > 300:
            acao = "Nivel de gas elevado detectado! Ventilando area..."
        print(acao)
        DeviceAction.log('Detector de Gas', acao, gas_level)

class Lamp(Subscriber):
    def __init__(self, broker):
        self.broker = broker

    def update(self, light_level):
        """
        Atualiza o estado da lâmpada com base no nivel de luminosidade recebido.
        Liga a lâmpada se a luminosidade estiver baixa, desliga se estiver suficiente.
        """
        acao = "Nivel de luz suficiente."
        if light_level < 300:
            acao = "Baixa luminosidade detectada! Ligando a lâmpada..."
        else:
            acao = "Luminosidade suficiente detectada! Desligando a lâmpada..."
        print(acao)
        DeviceAction.log('Lâmpada', acao, light_level)
