from flask import Flask, render_template, jsonify, request
from home_monitoring import MessageBroker, TemperatureSensor, HumiditySensor, MotionSensor, GasSensor, LightSensor
from home_monitoring.models import SensorData, DeviceAction, SensorState
from home_monitoring.sensors import GasDetector, Humidifier, Lamp, SecurityAlarm, SmartThermostat, Sprinkler

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sensor_data')
def sensor_data():
    data = SensorData.get_all()
    return render_template('data.html', data=data, title="Sensor Data")

@app.route('/device_actions')
def device_actions():
    actions = DeviceAction.get_all()
    return render_template('data.html', data=actions, title="Device Actions")

@app.route('/simulate_sensor_data', methods=['POST'])
def simulate_sensor_data_route():
    simulate_sensor_data()
    return jsonify({"message": "Sensor data simulated successfully!"}), 200

@app.route('/api/sensor_data')
def api_sensor_data():
    data = SensorData.get_all()
    return jsonify([dict(row) for row in data])

@app.route('/api/device_actions')
def api_device_actions():
    actions = DeviceAction.get_all()
    return jsonify([dict(row) for row in actions])

# Route to manually update sensor values
@app.route('/update_sensor', methods=['POST'])
def update_sensor():
    sensor_type = request.json.get('sensor_type')
    value = request.json.get('value')
    broker = MessageBroker.get_instance()
    broker.publish(sensor_type, value)
    return jsonify({"message": f"{sensor_type} updated to {value}"}), 200

from apscheduler.schedulers.background import BackgroundScheduler
import random

# Function to simulate sensor data updates with throttling
def simulate_sensor_data():
    temp_sensor.read_temperature()
    humidity_sensor.read_humidity()
    motion_sensor.detect_motion()
    gas_sensor.detect_gas()
    light_sensor.read_light()

if __name__ == '__main__':
    # Create broker instance and sensors/devices
    broker = MessageBroker.get_instance()
    temp_sensor = TemperatureSensor(broker)
    humidity_sensor = HumiditySensor(broker)
    motion_sensor = MotionSensor(broker)
    gas_sensor = GasSensor(broker)
    light_sensor = LightSensor(broker)
    
    thermostat = SmartThermostat(broker)
    humidifier = Humidifier(broker)
    alarm = SecurityAlarm(broker)
    gas_detector = GasDetector(broker)
    sprinkler = Sprinkler(broker)
    lamp = Lamp(broker)

    broker.subscribe('temperature', thermostat)
    broker.subscribe('humidity', humidifier)
    broker.subscribe('motion', alarm)
    broker.subscribe('gas', gas_detector)
    broker.subscribe('light', lamp)
    broker.subscribe('humidity', sprinkler)
    broker.subscribe('temperature', sprinkler)

    # Schedule sensor data simulation with throttling
    # scheduler = BackgroundScheduler()
    # # Example interval between 30 and 60 seconds
    # scheduler.add_job(simulate_sensor_data, 'interval', seconds=random.randint(30, 60))
    # scheduler.start()

    app.run(debug=True)
