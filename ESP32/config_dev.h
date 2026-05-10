#ifndef CONFIG_H
#define CONFIG_H

// Dados da rede Wi-Fi
const char* WIFI_SSID = "NOME_DA_REDE";
const char* WIFI_PASS = "SENHA_DA_REDE";

// Dados do broker MQTT
const char* MQTT_BROKER = "192.168.X.XXX";
const int   MQTT_PORT = XXXX;
const char* TOPIC_PUB = "cidade/inteligente/leds_status";

WiFiClient espClient;
PubSubClient client(espClient);

// Configurações de tempo
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = -10800; // GMT-3
const int   daylightOffset_sec = 0; // Horario de verão 


#endif