from crewai import Agent, Task, Crew, Process
import paho.mqtt.client as mqtt
import queue


analista = Agent(
    role="Analista de dados de luminosidade",
    goal=(
        "Analisar os dados de luminosidade recebidos do sensor, "
        "identificar se estão dentro ou fora da especificação e "
        "gerar um relatório direcionado ao setor responsável."
    ),
    backstory=(
        "Você é um analista especializado no monitoramento de sensores "
        "de luminosidade em ambientes industriais. Sua função é analisar "
        "as leituras recebidas, compará-las com a especificação definida "
        "e identificar possíveis situações que necessitem de atenção. "
        "Valores entre 100 e 1000 lux estão dentro da especificação. "
        "Valores abaixo de 100 lux ou acima de 1000 lux estão fora da "
        "especificação."
    ),
    verbose=True
)


analisar_luminosidade = Task(
    description=(
        '''
        Analise o dado de luminosidade recebido do sensor:

        {luminosidade}

        A especificação do sensor é:
        - Entre 100 e 1000 lux: DENTRO DA ESPECIFICAÇÃO;
        - Abaixo de 100 lux ou acima de 1000 lux: FORA DA ESPECIFICAÇÃO.

        Com base no dado recebido:

        1. Identifique o valor de luminosidade;
        2. Determine se o valor está dentro ou fora da especificação;
        3. Caso esteja FORA da especificação, gere um relatório
           direcionado à equipe de sustentação, descrevendo a situação
           identificada e a necessidade de atenção;
        4. Caso esteja DENTRO da especificação, gere um relatório
           direcionado à direção, apresentando os impactos positivos
           das condições adequadas de luminosidade.
        '''
    ),
    expected_output=(
        "Um relatório em Markdown contendo o valor de luminosidade, "
        "a classificação (dentro ou fora da especificação), o setor "
        "destinatário e a análise correspondente à situação identificada."
    ),
    agent=analista
)


equipe = Crew(
    agents=[analista],
    tasks=[analisar_luminosidade],
    process=Process.sequential,
    verbose=True
)

# ===== Conexao com ESP32 via MQTT =====

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "topico01"

fila_leituras = queue.Queue()


def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker MQTT, código:", rc)
    resultado_subscribe = client.subscribe(MQTT_TOPIC)
    print("Resultado do subscribe (result, mid):", resultado_subscribe)


def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Inscrição confirmada pelo broker! mid={mid}, qos={granted_qos}")

def on_message(client, userdata, msg):
    valor = msg.payload.decode()
    print(f"Luminosidade recebida do ESP: {valor}")
    fila_leituras.put(valor)


# versão mais recente do paho-mqtt precisa falar a versão da API de callback ao criar Client - da erro ou warning
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.enable_logger() 

client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_start()
 
try:
    while True:
        valor = fila_leituras.get()
 
        resultado = equipe.kickoff(
            inputs={
                "luminosidade": f"{valor} lux"
            }
        )
        print(resultado)
 
except KeyboardInterrupt:
    print("Encerrando...")
    client.loop_stop()
    client.disconnect()