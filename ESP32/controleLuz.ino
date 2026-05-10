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
    if(verificarLuz() && (timeinfo.tm_hour >= 18 || timeinfo.tm_hour < 6))
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

void ligarManual()
{
  bloqueioManual(true); 

  digitalWrite(LED1, HIGH);
  digitalWrite(LED2, HIGH);
  digitalWrite(LED3, HIGH);
}

void desligarManual()
{
  bloqueioManual(true); 

  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
  digitalWrite(LED3, LOW);
}

bool bloqueioManual(bool acionar = false) 
{
  static bool bloqueioAtivo = false;
  static time_t timestampLiberacao = 0;

  time_t agora = time(nullptr);

  if (acionar && !bloqueioAtivo){ 
    bloqueioAtivo = true;
    
    struct tm *infoTempo = localtime(&agora);
    infoTempo->tm_hour = 6;
    infoTempo->tm_min = 0;
    infoTempo->tm_sec = 0;
    infoTempo->tm_mday += 1;

    timestampLiberacao = mktime(infoTempo);
  }

  
  if (bloqueioAtivo){
    if (agora >= timestampLiberacao){
      bloqueioAtivo = false; 
    }
  }

  return bloqueioAtivo; 
}