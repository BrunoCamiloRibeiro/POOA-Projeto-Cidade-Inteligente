void conexaoWiFi()
{
  Serial.printf("Conectando a %s ", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }
  Serial.println(" CONECTADO!");
}

void callback(char* topic, byte* payload, unsigned int length) {
  StaticJsonDocument<200> doc;
  deserializeJson(doc, payload, length);

  String acao = doc["acao"];
  String bairro = doc["bairro"];

  if(bairro != Bairro) {
    return;
  }

  if (acao == "ligar_manual"  ) {
    ligarManual();
  } else if (acao == "desligar_manual") {
    desligarManual();
  } else if (acao == "resetar_sistema"){
    ESP.restart();
  } else{
    Serial.println("Ação desconhecida recebida: " + acao);
  }
}

void reconectar()
{
  while (!client.connected()) {
    Serial.print("Tentando conectar ao broker no Raspberry Pi...");
    String clientId = "ESP32_LogicaTempo";
    
    if (client.connect(clientId.c_str())) {
      Serial.println(" Conectado ao MQTT!");
    } else {
      Serial.print(" Falhou, erro: ");
      Serial.print(client.state());
      Serial.println(" Tentando novamente em 5s...");
      delay(5000);
    }
  }
}

