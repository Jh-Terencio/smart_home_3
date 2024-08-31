from flask import Flask, render_template, jsonify, request
from home_monitoring import MessageBroker, TemperatureSensor, HumiditySensor, MotionSensor, GasSensor, LightSensor
from home_monitoring.models import SensorData, DeviceAction, SensorState
from home_monitoring.sensors import GasDetector, Humidifier, Lamp, SecurityAlarm, SmartThermostat

app = Flask(__name__)  # inicializa a aplicacao Flask

# rota para obter as condicoes atuais dos sensores como JSON
@app.route('/api/current_conditions')
def current_conditions():
    sensor_data = SensorState.get_all()  # obtem o estado atual de todos os sensores
    data = {sensor['sensor_name']: sensor['last_value'] for sensor in sensor_data}  # constroi um dicionario com os valores dos sensores
    
    return jsonify({
        'temperature': data.get('temperature', None),
        'humidity': data.get('humidity', None),
        'motion': data.get('motion', None),
        'gas': data.get('gas', None),
        'light': data.get('light', None),
    })

# rota principal que renderiza a pagina inicial
@app.route('/')
def index():
    return render_template('index.html')  # ienderiza o template 'index.html'

# rota para visualizar os dados dos sensores
@app.route('/sensor_data')
def sensor_data():
    data = SensorData.get_all()  # rbtem todos os dados dos sensores
    return render_template('data.html', data=data, title="Sensor Data")

# rota para visualizar as acoes dos dispositivos
@app.route('/device_actions')
def device_actions():
    actions = DeviceAction.get_all()  # rbtem todas as acoes dos dispositivos
    return render_template('data.html', data=actions, title="Device Actions")

# rota para simular dados dos sensores
@app.route('/simulate_sensor_data', methods=['POST'])
def simulate_sensor_data_route():
    simulate_sensor_data()  # rhama a funcao que simula os dados dos sensores
    return jsonify({"message": "Sensor data simulated successfully!"}), 200

# rota para obter os dados dos sensores via API
@app.route('/api/sensor_data')
def api_sensor_data():
    data = SensorData.get_all()  # Obtem todos os dados dos sensores
    return jsonify([dict(row) for row in data])

# rota para obter as acoes dos dispositivos via API
@app.route('/api/device_actions')
def api_device_actions():
    actions = DeviceAction.get_all()  # obtem todas as acoes dos dispositivos
    return jsonify([dict(row) for row in actions])

# Rota para atualizar o valor de um sensor manualmente via API
@app.route('/update_sensor', methods=['POST'])
def update_sensor():
    sensor_type = request.json.get('sensor_type')  # obtem o tipo de sensor a ser atualizado
    value = request.json.get('value')  # obtem o novo valor do sensor
    broker = MessageBroker.get_instance()  # obtem a instancia do MessageBroker
    broker.publish(sensor_type, value)  # oublica a atualizacao no broker
    return jsonify({"message": f"{sensor_type} updated to {value}"}), 200

from apscheduler.schedulers.background import BackgroundScheduler
import random

# funcao que simula a leitura de dados dos sensores
def simulate_sensor_data():
    temp_sensor.read_temperature()
    humidity_sensor.read_humidity()
    motion_sensor.detect_motion()
    gas_sensor.detect_gas()
    light_sensor.read_light()

if __name__ == '__main__':
    broker = MessageBroker.get_instance()  # Inicializa o broker de mensagens

    # inicializa os sensores
    temp_sensor = TemperatureSensor(broker)
    humidity_sensor = HumiditySensor(broker)
    motion_sensor = MotionSensor(broker)
    gas_sensor = GasSensor(broker)
    light_sensor = LightSensor(broker)
    
    # inicializa os dispositivos que responderao aos sensores
    thermostat = SmartThermostat(broker)
    humidifier = Humidifier(broker)
    alarm = SecurityAlarm(broker)
    gas_detector = GasDetector(broker)
    lamp = Lamp(broker)

    # inscreve os dispositivos nos topicos correspondentes
    broker.subscribe('temperature', thermostat)
    broker.subscribe('humidity', humidifier)
    broker.subscribe('motion', alarm)
    broker.subscribe('gas', gas_detector)
    broker.subscribe('light', lamp)

    app.run(debug=True)  # inicia a aplicacao Flask em modo debug
