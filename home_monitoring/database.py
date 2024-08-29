# home_monitoring/database.py
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('home_monitoring.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_name TEXT NOT NULL UNIQUE,
            last_value REAL,
            last_update TEXT
        )
    ''')
    conn.commit()
    conn.close()
