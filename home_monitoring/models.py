# home_monitoring/models.py
from datetime import datetime
from .database import get_db_connection

class SensorData:
    @staticmethod
    def log(sensor_type, value):
        conn = get_db_connection()
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO sensor_data (sensor_type, value, timestamp)
            VALUES (?, ?, ?)
        ''', (sensor_type, value, timestamp))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC')
        data = cursor.fetchall()
        conn.close()
        return data

class DeviceAction:
    @staticmethod
    def log(device_name, action):
        conn = get_db_connection()
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO device_actions (device_name, action, timestamp)
            VALUES (?, ?, ?)
        ''', (device_name, action, timestamp))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM device_actions ORDER BY timestamp DESC')
        actions = cursor.fetchall()
        conn.close()
        return actions

class SensorState:
    @staticmethod
    def update(sensor_name, last_value):
        conn = get_db_connection()
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO sensors (sensor_name, last_value, last_update)
            VALUES (?, ?, ?)
            ON CONFLICT(sensor_name) DO UPDATE SET
            last_value=excluded.last_value, last_update=excluded.last_update
        ''', (sensor_name, last_value, timestamp))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sensors')
        sensors = cursor.fetchall()
        conn.close()
        return sensors
