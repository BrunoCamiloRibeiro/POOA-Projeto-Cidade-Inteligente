void adicionarLedNoJson(JsonArray& arrayLeds, int led, int transistor) {
    
    JsonObject objLed = arrayLeds.createNestedObject();
    
    objLed["luz"] = retornaNumeroLed(led);
    objLed["status"] = verificaIntegridadeLuz(led, transistor);
}

String gerarPacoteMqtt()
{
  StaticJsonDocument<512> doc; 
  
  doc["data_hora"] = obterData(); 
  doc["bairro"] = "ESP32_Bairro";
  
  JsonArray listaLeds = doc.createNestedArray("leds");
  
  adicionarLedNoJson(listaLeds, LED1, TRAN1);
  adicionarLedNoJson(listaLeds, LED2, TRAN2);
  adicionarLedNoJson(listaLeds, LED3, TRAN3);

  String buffer;
  serializeJson(doc, buffer);
  
  return buffer; 
}