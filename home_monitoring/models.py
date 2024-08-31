# home_monitoring/models.py

from datetime import datetime
from .database import get_db_connection

# Classe responsavel por registrar e recuperar dados de sensores no banco de dados
class SensorData:
    @staticmethod
    def log(sensor_type, value):
        """
        Registra um novo dado de sensor no banco de dados.
        :param sensor_type: Tipo de sensor (e.g., 'temperatura', 'umidade')
        :param value: Valor lido pelo sensor
        """
        conn = get_db_connection()  # Estabelece conexao com o banco de dados
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtem o timestamp atual
        cursor.execute('''
            INSERT INTO sensor_data (sensor_type, value, timestamp)
            VALUES (?, ?, ?)
        ''', (sensor_type, value, timestamp))  # Insere o dado no banco de dados
        conn.commit()  # Confirma a transacao
        conn.close()  # Fecha a conexao com o banco de dados

    @staticmethod
    def get_all():
        """
        Recupera todos os dados de sensores armazenados no banco de dados, ordenados por timestamp.
        :return: Lista de registros de dados de sensores
        """
        conn = get_db_connection()  
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC')  # Seleciona todos os dados de sensores
        data = cursor.fetchall()  # Recupera todos os registros
        conn.close()  # Fecha a conexao com o banco de dados
        return data  # Retorna os dados

# Classe responsavel por registrar e recuperar acoes dos dispositivos no banco de dados
class DeviceAction:
    @staticmethod
    def log(device_name, action, last_value):
        """
        Registra uma nova acao de dispositivo no banco de dados.
        :param device_name: Nome do dispositivo (e.g., 'Termostato Inteligente')
        :param action: Acao realizada pelo dispositivo (e.g., 'Ligando o ar condicionado...')
        :param last_value: ultimo valor que acionou a acao (e.g., temperatura)
        """
        conn = get_db_connection()  
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        cursor.execute('''
            INSERT INTO device_actions (device_name, action, last_value, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (device_name, action, last_value, timestamp))  # Insere a acao no banco de dados
        conn.commit()  # Confirma a transacao
        conn.close()  # Fecha a conexao com o banco de dados

    @staticmethod
    def get_all():
        """
        Recupera todas as acoes de dispositivos armazenadas no banco de dados, ordenadas por timestamp.
        :return: Lista de registros de acoes de dispositivos
        """
        conn = get_db_connection()  
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM device_actions ORDER BY timestamp DESC')  # Seleciona todas as acoes de dispositivos
        actions = cursor.fetchall()  # Recupera todos os registros
        conn.close()  # Fecha a conexao com o banco de dados
        return actions  # Retorna as acoes

# Classe responsavel por atualizar e recuperar o estado dos sensores no banco de dados
class SensorState:
    @staticmethod
    def update(sensor_name, last_value):
        """
        Atualiza o estado atual de um sensor no banco de dados.
        Se o sensor ja existir, atualiza seu valor e timestamp; caso contrario, insere um novo registro.
        :param sensor_name: Nome do sensor (e.g., 'Sensor de Temperatura')
        :param last_value: ultimo valor lido pelo sensor
        """
        conn = get_db_connection()  
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        cursor.execute('''
            INSERT INTO sensors (sensor_name, last_value, last_update)
            VALUES (?, ?, ?)
            ON CONFLICT(sensor_name) DO UPDATE SET
            last_value=excluded.last_value, last_update=excluded.last_update
        ''', (sensor_name, last_value, timestamp))  # Insere ou atualiza o estado do sensor
        conn.commit()  
        conn.close()  

    @staticmethod
    def get_all():
        """
        Recupera os estados atuais de todos os sensores armazenados no banco de dados.
        :return: Lista de registros de estados de sensores
        """
        conn = get_db_connection()  
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sensors') 
        sensors = cursor.fetchall() 
        conn.close()
        return sensors 
