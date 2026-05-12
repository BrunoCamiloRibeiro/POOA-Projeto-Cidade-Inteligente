import json
import time
import random
from datetime import datetime
import paho.mqtt.client as mqtt

BROKER = "broker.emqx.io" 
TOPIC_PUB = "cidade/bairros/status"
BAIRROS = ["Centro", "Zona Norte", "Jardim das Acácias", "Vila Nova"]
STATUS_OPCOES = ["Ligado", "Desligado", "Queimado"]

# Pesos: 50% de chance de estar Ligado, 40% Desligado, 10% Queimado
PESOS = [50, 40, 10] 

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Simulador conectado! Enviando dados estruturados...")

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect

try:
    mqtt_client.connect(BROKER, 1883, 60)
    mqtt_client.loop_start()

    while True:
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bairro = random.choice(BAIRROS)
        luminosidade = random.randint(10, 100)
        
        # Estrutura de objeto em JSON no lugar do bool
        l1 = {"Luz": 1, "Status": random.choices(STATUS_OPCOES, weights=PESOS)[0]}
        l2 = {"Luz": 2, "Status": random.choices(STATUS_OPCOES, weights=PESOS)[0]}
        l3 = {"Luz": 3, "Status": random.choices(STATUS_OPCOES, weights=PESOS)[0]}
        
        # Falha crítica: 1 em 15 de chance de queimar todas as luzes
        if random.randint(1, 15) == 1:
            l1["Status"] = l2["Status"] = l3["Status"] = "Queimado"

        # Monta a nova lista com os dicionários dentro
        payload_list = [data_hora, bairro, luminosidade, l1, l2, l3]
        payload_json = json.dumps(payload_list, ensure_ascii=False)

        mqtt_client.publish(TOPIC_PUB, payload_json)
        print(f"Enviado: {payload_json}")
        
        time.sleep(4)

except KeyboardInterrupt:
    print("\nEncerrado.")
finally:
    mqtt_client.loop_stop()
    mqtt_client.disconnect()