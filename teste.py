import sqlite3
import random
from datetime import datetime

# Singleton Pattern for Message Broker
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
            self.create_tables()

    def get_db_connection(self):
        conn = sqlite3.connect('home_monitoring.db')
        conn.row_factory = sqlite3.Row
        return conn

    def create_tables(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_type TEXT NOT NULL,
                value REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_name TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def subscribe(self, topic, subscriber):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(subscriber)

    def publish(self, topic, message):
        if topic in self.subscribers:
            self.log_sensor_data(topic, message)
            for subscriber in self.subscribers[topic]:
                if isinstance(subscriber, Sprinkler):
                    # Handle the sprinkler's need for both humidity and temperature
                    if topic == 'humidity':
                        subscriber.update(humidity=message)
                    elif topic == 'temperature':
                        subscriber.update(temperature=message)
                else:
                    subscriber.update(message)

    def log_sensor_data(self, sensor_type, value):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO sensor_data (sensor_type, value, timestamp)
            VALUES (?, ?, ?)
        ''', (sensor_type, value, timestamp))
        conn.commit()
        conn.close()

    def log_device_action(self, device_name, action):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO device_actions (device_name, action, timestamp)
            VALUES (?, ?, ?)
        ''', (device_name, action, timestamp))
        conn.commit()
        conn.close()

    def get_sensor_data(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sensor_data')
        data = cursor.fetchall()
        conn.close()
        return data

    def get_device_actions(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM device_actions')
        actions = cursor.fetchall()
        conn.close()
        return actions

# Observer Pattern for Subscribers
class Subscriber:
    def update(self, message):
        raise NotImplementedError("Subscribers must implement the update method.")

# Proxy Pattern for Sensors (Publishers)
class SensorProxy:
    def __init__(self, broker):
        self.broker = broker

    def publish_data(self, topic, data):
        self.broker.publish(topic, data)

# Implementação de Sensores com valores aleatórios e arredondamento
class TemperatureSensor(SensorProxy):
    def read_temperature(self):
        temperature = round(random.uniform(15.0, 35.0), 2)  # Simula a leitura de temperatura aleatória entre 15 e 35 graus
        self.publish_data('temperature', temperature)

class HumiditySensor(SensorProxy):
    def read_humidity(self):
        humidity = round(random.uniform(20.0, 80.0), 2)  # Simula a leitura de umidade aleatória entre 20% e 80%
        self.publish_data('humidity', humidity)

class MotionSensor(SensorProxy):
    def detect_motion(self):
        motion_detected = random.choice([0, 1])  # Simula a detecção de movimento (0 para nenhum, 1 para detectado)
        self.publish_data('motion', motion_detected)

class GasSensor(SensorProxy):
    def detect_gas(self):
        gas_level = round(random.uniform(100, 500), 2)  # Simula a leitura do nível de gás entre 100 e 500 ppm
        self.publish_data('gas', gas_level)

class LightSensor(SensorProxy):
    def read_light(self):
        light_level = round(random.uniform(0, 1000), 2)  # Simula a leitura de luminosidade entre 0 e 1000 lux
        self.publish_data('light', light_level)

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
        self.broker.log_device_action('Smart Thermostat', action)

class Humidifier(Subscriber):
    def __init__(self, broker):
        self.broker = broker

    def update(self, humidity):
        action = "Humidity is at a good level."
        if humidity < 40:
            action = "Turning on the humidifier..."
        print(action)
        self.broker.log_device_action('Humidifier', action)

class SecurityAlarm(Subscriber):
    def __init__(self, broker):
        self.broker = broker

    def update(self, motion_detected):
        action = "No motion detected."
        if motion_detected:
            action = "Motion detected! Triggering alarm..."
        print(action)
        self.broker.log_device_action('Security Alarm', action)

class GasDetector(Subscriber):
    def __init__(self, broker):
        self.broker = broker

    def update(self, gas_level):
        action = "Gas level normal."
        if gas_level > 300:
            action = "High gas level detected! Ventilating area..."
        print(action)
        self.broker.log_device_action('Gas Detector', action)

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
            self.broker.log_device_action('Sprinkler', action)

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
        self.broker.log_device_action('Lamp', action)

# Exemplo de uso
if __name__ == "__main__":
    broker = MessageBroker.get_instance()

    # Criando sensores
    temp_sensor = TemperatureSensor(broker)
    humidity_sensor = HumiditySensor(broker)
    motion_sensor = MotionSensor(broker)
    gas_sensor = GasSensor(broker)
    light_sensor = LightSensor(broker)

    # Criando dispositivos
    thermostat = SmartThermostat(broker)
    humidifier = Humidifier(broker)
    alarm = SecurityAlarm(broker)
    gas_detector = GasDetector(broker)
    sprinkler = Sprinkler(broker)
    lamp = Lamp(broker)

    # Assinando dispositivos aos tópicos dos sensores
    broker.subscribe('temperature', thermostat)
    broker.subscribe('humidity', humidifier)
    broker.subscribe('motion', alarm)
    broker.subscribe('gas', gas_detector)
    broker.subscribe('light', lamp)

    # Assinando o sprinkler para ouvir tanto umidade quanto temperatura
    broker.subscribe('humidity', sprinkler)
    broker.subscribe('temperature', sprinkler)

    # Simulando leituras dos sensores
    temp_sensor.read_temperature()
    humidity_sensor.read_humidity()
    motion_sensor.detect_motion()
    gas_sensor.detect_gas()
    light_sensor.read_light()

