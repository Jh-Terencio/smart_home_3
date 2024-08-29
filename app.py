from flask import Flask, render_template, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('home_monitoring.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sensor_data')
def sensor_data():
    conn = get_db_connection()
    sensor_data = conn.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template('data.html', data=sensor_data, title="Sensor Data")

@app.route('/device_actions')
def device_actions():
    conn = get_db_connection()
    device_actions = conn.execute('SELECT * FROM device_actions ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template('data.html', data=device_actions, title="Device Actions")

@app.route('/api/sensor_data')
def api_sensor_data():
    conn = get_db_connection()
    sensor_data = conn.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in sensor_data])

@app.route('/api/device_actions')
def api_device_actions():
    conn = get_db_connection()
    device_actions = conn.execute('SELECT * FROM device_actions ORDER BY timestamp DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in device_actions])

if __name__ == '__main__':
    app.run(debug=True)
