# home_monitoring/__init__.py
from .database import create_tables
from .broker import MessageBroker
from .sensors import (TemperatureSensor, HumiditySensor, MotionSensor, GasSensor, LightSensor,
                      SmartThermostat, Humidifier, SecurityAlarm, GasDetector, Lamp)

# Initialize the tables when the package is imported
create_tables()
