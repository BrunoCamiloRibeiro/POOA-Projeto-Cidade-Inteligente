<div align="center">
  
# Sistema Inteligente de Controle e Manutenção da Iluminação Pública
### Projeto Final - Programação Avançada Orientada a Objetos (PAOO)
### CST em Análise e Desenvolvimento de Sistemas - Fatec Rio Preto

</div>

<br>

**Professor:** Mário Henrique de Souza Pardo

**Equipe:** Audrey Eduardo Ribeiro de Oliveira e Souza, Bruno Camilo Ribeiro, João Pedro Pohlmann Neo, Matheus Henrique Pozeti de Faria

---

## 1. Problema e Objetivo do Projeto
Atualmente, a identificação de falhas na iluminação pública urbana depende predominantemente de notificações feitas pela população. Além disso, o sistema apresenta baixa eficiência energética, operando com horários fixos de acionamento que desconsideram as condições reais de luminosidade e as necessidades específicas de cada local. A demora na manutenção pode gerar externalidades negativas, como o aumento da criminalidade e desvalorização imobiliária.

O **objetivo** deste projeto é desenvolver um sistema de gestão automatizada para iluminação pública urbana (dentro do tema de *Cidades Inteligentes*). Utilizando uma arquitetura IoT em nós (Edge) e um servidor central, o projeto controla o acionamento de luminárias LED, detecta autonomamente falhas (lâmpadas queimadas) e reage às condições reais de luminosidade.

---

## 2. Arquitetura e Estratégia de Firmware

O sistema utiliza uma topologia IoT em estrela baseada no protocolo MQTT via Wi-Fi. 
* **Nós de Borda (ESP32 e ESP8266):** Atuam realizando a leitura de sensores LDR e controlando o estado de 3 LEDs em cada nó. A detecção de LEDs queimados é feita por transistores NPN configurados em malha fechada. Se um LED falha, o transistor entra em corte, fazendo com que o pino de leitura do microcontrolador (em modo PULLUP) retorne nível lógico ALTO (HIGH).
* **Nó Central (Raspberry Pi Zero W):** Centraliza a inteligência como Broker Mosquitto e interface de controle principal (Dashboard Cloud/Local).
* **Software:** O firmware dos nós é modular e não-bloqueante, utilizando a função `millis()` nativa do C/C++ para processar mensagens JSON e ler os sensores simultaneamente, garantindo respostas em tempo real.

---

## 3. Regras de Negócio do Sistema

O comportamento do sistema obedece ao seguinte escalonamento e lógica de automação:

* **SE** (Saída digital == HIGH E Leitura Transistor == HIGH) **ENTÃO** Publicar alerta de "Lâmpada Queimada" no tópico MQTT correspondente.
* **SENÃO** Publicar informação de "Lâmpada OK".
* **SE** (Valor LDR < N E HoraAtual > 18:00) **ENTÃO** Enviar comando para LIGAR LEDs.
* **SENÃO SE** (Hora_Atual > 06:00) **ENTÃO** Enviar comando para DESLIGAR LEDs.
* **SE** (Receber alerta via MQTT) **ENTÃO** Registrar log, exibir na interface e acender LED_Alerta_1.
* **SE** (Tempo Falha > N) **ENTÃO** Manter alertas ativos e acender LED_Alerta_2.
* **SE** (Tempo Falha > 2N) **ENTÃO** Manter alertas ativos e acender LED_Alerta_3.
* **SE** (Tempo Falha > 3N) **ENTÃO** Ativar Buzzer (Alerta Crítico).
* **SE** (Botão Ligar Manual == PRESSIONADO) **ENTÃO** Forçar estado HIGH nos LEDs e suspender rotina automática até a "Virada de Dia" (00:00).
* **SE** (Botão Desligar Manual == PRESSIONADO) **ENTÃO** Forçar estado LOW nos LEDs e suspender rotina automática até a "Virada de Dia" (00:00).
* **SE** (Botão Reset == PRESSIONADO) **ENTÃO** Publicar comando de "System Reboot" para todos os Clientes MQTT (ESPs).

---

## 4. Lista de Componentes Usados e Orçamento

| Componente | Quant. | Função no Projeto | Preço Total |
| :--- | :---: | :--- | :--- |
| **Raspberry Pi Zero W** | 1 | Servidor central (Broker) e painel de controle físico. | R$ 180,00 |
| **Placa ESP32** | 1 | Nó de borda (Lê falhas nos LEDs, controla e envia dados). | R$ 38,00 |
| **Placa ESP8266** | 1 | Nó de borda (Lê falhas nos LEDs, controla e envia dados). | R$ 30,00 |
| **Cartão MicroSD**| 1 | Armazenar o sistema operacional do Raspberry Pi. | R$ 35,00 |
| **LEDs** | 9 | 3 para o ESP32, 3 para o ESP8266, 3 de alerta para o Pi. | R$ 6,00 |
| **Resistores** | 9 | Limitar corrente dos 9 LEDs do projeto. | R$ 5,00 |
| **Transistores NPN (BC548)** | 6 | Malha fechada para detectar queima dos LEDs. | R$ 10,00 |
| **LDR**| 2 | Medir a luminosidade ambiente nos nós. | R$ 14,00 |
| **Push button** | 3 | Controles físicos manuais para o painel do Raspberry Pi. | R$ 4,00 |
| **Buzzer** | 1 | Alerta sonoro (Crítico) no Raspberry Pi. | R$ 3,00 |
| **Protoboards** | 3 | Montagem dos circuitos. | R$ 150,00 |
| **Kit de Fios** | 1 | Conexões físicas dos componentes. | R$ 30,00 |
| **Custo Total do Projeto** | - | - | **R$ 505,00** |

---

## 5. Tecnologias Usadas
* **Hardware:** ESP32, ESP8266, Raspberry Pi Zero W, Sensores e Atuadores discretos.
* **Comunicação:** Wi-Fi, Protocolo MQTT (Eclipse Mosquitto).
* **Firmware (Nós):** C/C++ (modular, utilizando `millis()`).
* **Backend / Lógica Local:** Python (com bibliotecas de manipulação de GPIO). 
* **Frontend / Dashboard Cloud:** Dojo Toolkit, HTML5, CSS3, JavaScript.

---

## 6. Pinouts e Diagramas das Placas

#### *ESP32:*
<div align="center">
  <img src="https://www.upesy.com/cdn/shop/files/doc-esp32-pinout-reference-wroom-devkit.png" alt="Pinout ESP32" width="800">
</div>
> Fonte: https://www.upesy.com/blogs/tutorials/esp32-pinout-reference-gpio-pins-ultimate-guide

#### *ESP8266:*
<div align="center">
  <img src="https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2019/05/ESP8266-NodeMCU-kit-12-E-pinout-gpio-pin.png?resize=817%2C542&quality=100&strip=all&ssl=1" alt="Pinout ESP8266" width="800">
</div>
> Fonte: https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/

#### *Raspberry Pi Zero W*
<div align="center">
  <img src="https://images.wevolver.com/eyJidWNrZXQiOiJ3ZXZvbHZlci1wcm9qZWN0LWltYWdlcyIsImtleSI6ImZyb2FsYS8xNzY1MTYwNDM1NzQyLTE3NjUxNjA0MzU3NDIucG5nIiwiZWRpdHMiOnsicmVzaXplIjp7IndpZHRoIjo5NTAsImZpdCI6ImNvdmVyIn19fQ==" alt="Pinout Raspberry Pi Zero W" width="800">
</div>
> Fonte: https://www.wevolver.com/article/raspberry-pi-zero-2-w-pinout-comprehensive-guide-for-engineers

---

*Repositório acadêmico desenvolvido para avaliação na disciplina de PAOO, Fatec Rio Preto.*

## 7. Esquema Eletrônico

<div align="center">
  <img src="assets\esquema_eletrico.png" alt="Esquema Eletrônico do Sistema IoT" width="1000">
</div>

