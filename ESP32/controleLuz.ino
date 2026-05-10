bool verificarLuz()
{
  if (analogRead(LDR) < LDR_ESCURO_DEFINICAO)
  {
    return true; // Está escuro
  }
  else
  {
    return false; // Está claro
  }
}

void controlePadrao()
{
  struct tm timeinfo;
  if (getLocalTime(&timeinfo)){

    if(verificarLuz() && timeinfo.tm_hour >= 18 || timeinfo.tm_hour < 6)
    {
      digitalWrite(LED1, HIGH);
      digitalWrite(LED2, HIGH);
      digitalWrite(LED3, HIGH);
    }
    else
    {
      digitalWrite(LED1, LOW);
      digitalWrite(LED2, LOW);
      digitalWrite(LED3, LOW);
    }
  }
}

int verificaIntegridadeLuz(int led, int transistor)
{
    if (digitalRead(led) == HIGH)
    {
        if (digitalRead(transistor) == HIGH)
        {
            return 1; 
        }
        else
        {
            return 2; 
        }
    }else{
        return 0;
    }
}


int retornaNumeroLed(int led)
{
   switch (led)
   {
      case LED1:
         return 1;
      case LED2:
         return 2;
      case LED3:
         return 3;
      default:
         return -1; 
   }
}