# home_monitoring/database.py

import sqlite3

def get_db_connection():
    """
    Estabelece e retorna uma conexao com o banco de dados SQLite 'home_monitoring.db'.
    A conexao utiliza a fabrica de linhas (row_factory) que permite o acesso aos dados
    atraves de nomes de colunas.
    :return: Conexao com o banco de dados SQLite
    """
    conn = sqlite3.connect('home_monitoring.db')
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn

def create_tables():
    """
    Cria as tabelas necessarias no banco de dados, se ainda nao existirem.
    As tabelas criadas sao:
    - sensor_data: Armazena os dados capturados pelos sensores.
    - device_actions: Armazena as acoes realizadas pelos dispositivos.
    - sensors: Armazena o estado atual de cada sensor.
    """
    conn = get_db_connection()  # Estabelece conexao com o banco de dados
    cursor = conn.cursor()

    # Criacao da tabela sensor_data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_type TEXT NOT NULL,
            value REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')

    # Criacao da tabela device_actions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT NOT NULL,
            action TEXT NOT NULL,
            last_value REAL,
            timestamp TEXT NOT NULL
        )
    ''')

    # Criacao da tabela sensors
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_name TEXT NOT NULL UNIQUE,
            last_value REAL,
            last_update TEXT
        )
    ''')

    conn.commit()  # Confirma a criacao das tabelas
    conn.close()  # Fecha a conexao com o banco de dados
