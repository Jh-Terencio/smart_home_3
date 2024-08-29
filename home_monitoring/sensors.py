# home_monitoring/sensors.py
import random
from .broker import MessageBroker
from .models import DeviceAction

class SensorProxy:
    def __init__(self, broker):
        self.broker = broker
        self.last_published_values = {}

    def publish_data(self, topic, data, threshold=0.1):
        last_value = self.last_published_values.get(topic)
        if last_value is None or abs(data - last_value) > threshold:
            self.broker.publish(topic, data)
            self.last_published_values[topic] = data

# Implementação de Sensores with conditional logging
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
        light_level = round(random.uniform(0, 1000), 2)
        self.publish_data('light', light_level, threshold=20.0)

# Observer Pattern for Subscribers
class Subscriber:
    def update(self, message):
        raise NotImplementedError("Subscribers must implement the update method.")

# Implementação de Dispositivos
class SmartThermostat(Subscriber):
    def __init__(self, broker):
        self.broker = broker

    def update(self, temperature):
        action = "Temperature is comfortable."
        if temperature > 25:
            action = "Turning on the air conditioner..."
        elif temperature < 15:
            action = "Turning on the heater..."
        print(action)
        DeviceAction.log('Smart Thermostat', action)

class Humidifier(Subscriber):
    def __init__(self, broker):
        self.broker = broker

    def update(self, humidity):
        action = "Humidity is at a good level."
        if humidity < 40:
            action = "Turning on the humidifier..."
        print(action)
        DeviceAction.log('Humidifier', action)

class SecurityAlarm(Subscriber):
    def __init__(self, broker):
        self.broker = broker

    def update(self, motion_detected):
        action = "No motion detected."
        if motion_detected:
            action = "Motion detected! Triggering alarm..."
        print(action)
        DeviceAction.log('Security Alarm', action)

class GasDetector(Subscriber):
    def __init__(self, broker):
        self.broker = broker

    def update(self, gas_level):
        action = "Gas level normal."
        if gas_level > 300:
            action = "High gas level detected! Ventilating area..."
        print(action)
        DeviceAction.log('Gas Detector', action)

class Sprinkler(Subscriber):
    def __init__(self, broker):
        self.broker = broker
        self.humidity = None
        self.temperature = None

    def update(self, humidity=None, temperature=None):
        if humidity is not None:
            self.humidity = humidity
        if temperature is not None:
            self.temperature = temperature
        
        if self.humidity is not None and self.temperature is not None:
            action = "Conditions are normal."
            if self.humidity < 40 and self.temperature > 30:
                action = "Low humidity and high temperature detected! Activating sprinkler..."
            print(action)
            DeviceAction.log('Sprinkler', action)

class Lamp(Subscriber):
    def __init__(self, broker):
        self.broker = broker

    def update(self, light_level):
        action = "Light level is sufficient."
        if light_level < 300:
            action = "Low light detected! Turning on the lamp..."
        else:
            action = "Sufficient light detected! Turning off the lamp..."
        print(action)
        DeviceAction.log('Lamp', action)
