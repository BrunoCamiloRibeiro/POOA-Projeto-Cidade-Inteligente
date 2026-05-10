#include "pins.h"
#include "libs.h"
#include "config.h"
#include "consts.h"

void setup() 
{
  Serial.begin(115200);
  configPins();

  conexaoWiFi();

  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

  client.setServer(MQTT_BROKER, MQTT_PORT);
}

void loop() 
{
  if (!client.connected()) {
    reconectar();
  }

  client.loop();

  controlePadrao();
}


