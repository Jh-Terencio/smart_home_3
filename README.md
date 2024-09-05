# Home Monitoring Dashboard

## Descrição

O **Home Monitoring Dashboard** é um sistema para monitoramento residencial inteligente que utiliza sensores para coletar dados de ambiente como temperatura, umidade, movimento, gás e luminosidade. Esses dados são processados e utilizados para acionar dispositivos automatizados, como termostato, umidificador, lâmpadas, entre outros. A interface web permite visualizar o estado atual dos dispositivos e dos sensores, além de simular dados de sensores manualmente.

## Estrutura de Pastas

A estrutura do projeto é organizada da seguinte forma:


### Principais Funcionalidades

1. **Adicionar Dispositivos**
   - O usuário pode adicionar novos dispositivos à rede doméstica, como termostatos, umidificadores, alarmes de segurança, detectores de gás e lâmpadas.
   - Interface: `add_device.html`

2. **Configurar Sensores**
   - Permite configurar sensores que monitoram diferentes aspectos da casa, como temperatura, umidade, movimento, gás e luminosidade.
   - Interface: `configure_sensor.html`

3. **Monitoramento de Dados**
   - Exibe o histórico de dados capturados pelos sensores, permitindo ao usuário acompanhar as leituras em tempo real ou acessá-las posteriormente.
   - Interface: `data.html`

4. **Dashboard Interativo**
   - Apresenta um painel de controle que exibe os dispositivos e sensores configurados na rede. Inclui opções para simular dados de sensores e atualizar o estado dos dispositivos automaticamente com base nos dados recebidos.
   - Interface: `index.html`

### Como Funciona

- **Arquitetura Publish-Subscribe**: O sistema usa um barramento de mensagens onde sensores (publishers) enviam dados sobre o ambiente para tópicos específicos. Dispositivos (subscribers) se inscrevem nesses tópicos para reagir às mudanças ambientais de acordo com as configurações estabelecidas.

- **Simulação de Sensores**: Para fins de teste e desenvolvimento, o sistema inclui uma funcionalidade de simulação que permite gerar dados fictícios para os sensores. Esses dados são utilizados para acionar dispositivos como termostatos, alarmes e lâmpadas, conforme necessário.

### Cenários de Uso

1. **Automação de Iluminação**
   - As luzes podem ser automaticamente acesas ou apagadas com base nos níveis de luminosidade detectados pelo sensor de luz.

2. **Controle Automático de Temperatura**
   - O termostato ajusta a temperatura interna com base nas leituras dos sensores de temperatura, mantendo o ambiente confortável.

3. **Disparo de Alarmes**
   - O sistema pode ativar um alarme de segurança se for detectado movimento em áreas críticas da residência durante horários não programados.

### Tecnologias Utilizadas

- **Python**: Linguagem de programação principal do backend.
- **Flask**: Framework web utilizado para criar rotas e renderizar templates.
- **Jinja2**: Motor de templates utilizado para gerar HTML dinâmico.
- **JavaScript/jQuery**: Usado para interações dinâmicas no front-end.
- **HTML/CSS**: Para a estruturação e estilização das páginas web.

## Instalação

```bash
cd home_monitoring
python -m venv venv
cd ..
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
