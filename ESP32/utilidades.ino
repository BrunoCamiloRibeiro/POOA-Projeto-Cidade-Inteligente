String obterData() {
  struct tm timeinfo;
  
  if (!getLocalTime(&timeinfo)) {
    return "Erro_Data"; 
  }
  
  char bufferData[11]; 

  strftime(bufferData, sizeof(bufferData), "%d/%m/%Y", &timeinfo);
  
  return String(bufferData);
}