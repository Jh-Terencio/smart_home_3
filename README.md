# Smart Home Monitoring

## 1. Visão Geral do Projeto

**Nome:** Home Monitoring Dashboard

**Descrição:**

O Home Monitoring Dashboard é um sistema de monitoramento residencial inteligente projetado para coletar, processar e exibir dados ambientais de uma residência. Utilizando uma variedade de sensores (temperatura, umidade, movimento, gás e luminosidade), o sistema permite o monitoramento em tempo real e a automação de dispositivos como termostatos, lâmpadas e umidificadores. A interface web proporciona ao usuário uma visão centralizada dos dispositivos e sensores, além da capacidade de simular manualmente os dados dos sensores.

**Objetivo:**

Criar um sistema de monitoramento residencial inteligente que utiliza a arquitetura _publish-subscribe_ para integrar dispositivos IoT em uma rede doméstica, facilitando a automação de tarefas como controle de iluminação, alarme e controle de temperatura.

## 2. Arquitetura do Sistema

**Estilo de Arquitetura:** Publish-Subscribe

**Descrição:**

O sistema segue o paradigma _publish-subscribe_ (pub/sub), onde sensores e dispositivos IoT se comunicam através de um barramento de mensagens. Os sensores atuam como "publishers", enviando dados sobre o estado do ambiente para tópicos específicos. Os dispositivos que precisam reagir a essas informações se inscrevem como "subscribers" nesses tópicos, permitindo que respondam dinamicamente a mudanças no ambiente.

**Componentes Principais:**

- **Sensores:** Monitoram diversos aspectos da casa, como temperatura, umidade, luminosidade, movimento e presença de pessoas.
- **Dispositivos Automatizados:** Incluem termostatos, lâmpadas, umidificadores e alarmes.
- **Message Broker:** Gerencia a comunicação entre os sensores e os dispositivos automatizados.
- **Websockets:** Facilitam a comunicação em tempo real na interface web.
- **Interface Web:** Fornece uma visão centralizada dos dados do sistema e permite a configuração de dispositivos e a simulação de dados de sensores.

## 3. Componentes do Sistema

**Sensores:**

- **Sensor de Temperatura:** Publica a temperatura atual do ambiente em um tópico específico.
- **Sensor de Umidade:** Monitora e publica o nível de umidade.
- **Sensor de Movimento:** Detecta a presença de movimento e publica alertas.
- **Sensor de Gás:** Monitora a presença de gases perigosos.
- **Sensor de Luminosidade:** Mede o nível de luz no ambiente e publica esses dados.

**Dispositivos Automatizados:**

- **Termostato:** Se inscreve nos tópicos de temperatura e ajusta a climatização conforme necessário.
- **Lâmpadas Inteligentes:** Se inscrevem no tópico de luminosidade e ajustam a iluminação.
- **Umidificador:** Se inscreve nos tópicos de umidade para manter os níveis desejados.
- **Alarme:** Responde a dados de movimento ou presença de gases para disparar alertas de segurança.

**Interface Web:**

- **Dashboard:** Exibe o estado atual de todos os sensores e dispositivos.
- **Simulação de Sensores:** Permite ao usuário alterar e testar manualmente os dados de sensores.

## Instalação

1. Crie a venv (Ambiente virtual):

   ``` bash
   python -m venv venv
   ```

2. Ative a venv

   ``` bash
   venv\Scripts\activate
   ```

3. Instale as bibliotecas

   ``` bash
   pip install -r requirements.txt
   ```

4. Execute `python app.py` para executar o código:

   ``` bash
   python app.py
   ```
