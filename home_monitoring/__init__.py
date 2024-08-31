# home_monitoring/__init__.py
from .database import create_tables
from .broker import MessageBroker
from .sensors import (TemperatureSensor, HumiditySensor, MotionSensor, GasSensor, LightSensor,
                      SmartThermostat, Humidifier, SecurityAlarm, GasDetector, Lamp)

# Inicializa as tabelas
create_tables()
