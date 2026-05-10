void configPins()
{
  // Configura os pinos dos LEDs como saída
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);

  // Configura os pinos dos transistores como entrada pullup
  pinMode(TRAN1, INPUT_PULLUP);
  pinMode(TRAN2, INPUT_PULLUP);
  pinMode(TRAN3, INPUT_PULLUP);

  // Configura o pino do LDR como entrada
  pinMode(LDR, INPUT);
}