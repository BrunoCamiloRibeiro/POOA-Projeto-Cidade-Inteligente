<div align="center">
  
# Sistema de Monitoramento e Controle de LEDs via IoT
### 4º Semestre Fatec
  
</div>

---

## 1. Objetivo do projeto
Desenvolver um sistema de Internet das Coisas (IoT) em arquitetura de nós (Edge) e servidor central para monitoramento e controle de hardware. O projeto consiste em microcontroladores (ESP32 e ESP8266) que controlam o acionamento de LEDs, detectam fisicamente se estão operacionais ou queimados (utilizando transistores como sensores digitais) e medem a luminosidade do ambiente em porcentagem. Os dados são enviados via Wi-Fi para um Raspberry Pi Zero W, que atua como hub central, exibindo um dashboard interativo controlável por botões físicos locais. Uma segunda frente do dashboard rodará na nuvem utilizando o Dojo Toolkit.

---

## 2. Parte 1: Nó Principal (ESP32)

### 2.1 ESP32 - Leitura, Controle e Comunicação
Fazer o ESP32 ler o status dos componentes, controlar o acionamento e transmitir os dados. (Nota: Se o tempo for curto na integração geral, o plano de contingência é fazer o ESP32 se comunicar diretamente com o front-end em Dojo ou API similar).

### 2.2 Descrição do que a parte faz
O ESP32 é o nó principal de coleta de dados. Ele gerencia 3 LEDs locais, acendendo-os ou apagando-os conforme comandos recebidos. Simultaneamente, ele lê o sinal de 3 transistores NPN acoplados aos circuitos dos LEDs para verificar se a corrente está passando (LED OK) ou interrompida (LED Queimado). Além disso, converte o sinal analógico de um módulo LDR para calcular a porcentagem de luminosidade do ambiente. Transmite tudo via Wi-Fi (idealmente MQTT).

### 2.3 Componentes usados e preços

| Componente | Quantidade | Preço Unitário Médio | Preço Total Estimado |
| :--- | :---: | :--- | :--- |
| **Placa ESP32 (NodeMCU)** | 1 | R$ 45,00 | R$ 45,00 |
| **LEDs (5mm)** | 3 | R$ 0,20 | R$ 0,60 |
| **Resistores (220Ω ou 330Ω)** | 3 | R$ 0,10 | R$ 0,30 |
| **Transistores NPN (BC548)** | 3 | R$ 0,30 | R$ 0,90 |
| **Módulo Sensor de Luz LDR (com LM393)** | 1 | R$ 7,00 | R$ 7,00 |
| **Protoboard e Jumpers** | 1 | R$ 15,00 | R$ 15,00 |
| **Subtotal Estimado** | - | - | **~ R$ 68,80** |

### 2.4 Tecnologias usadas
* **Linguagem:** C/C++
* **Ambiente:** Arduino IDE
* **Bibliotecas:** `WiFi.h`, `PubSubClient.h` (para MQTT)

---

## 3. Parte 2: O Cérebro e Dashboard (Raspberry Pi)

### 3.1 A parte do Raspberry Pi, interface e controles
Hospedar a aplicação central, exibir a interface (Web local ou Nativa Python, a decidir), ler os controles físicos e agregar as informações da rede.

### 3.2 Descrição do que a parte faz
O Raspberry Pi Zero W atua como o servidor do sistema. Ele recebe os dados do ESP32 e ESP8266. Exibe um painel de controle (Dashboard) em um monitor. A interação com este dashboard é feita de forma "industrial", utilizando 4 botões físicos (Push Buttons) ligados aos pinos GPIO do Pi, sem necessidade de mouse/teclado. O painel físico do Pi também conta com 3 LEDs de status e um Buzzer que emite alertas sonoros caso o sistema detecte um LED queimado nos nós.

### 3.3 Componentes usados e preços

| Componente | Quantidade | Preço Unitário Médio | Preço Total Estimado |
| :--- | :---: | :--- | :--- |
| **Raspberry Pi Zero W** *(Já adquirido)* | 1 | R$ 180,00 | R$ 180,00 |
| **Cartão MicroSD (16GB/32GB)** | 1 | R$ 35,00 | R$ 35,00 |
| **Botões Push Button (Chave Tact)** | 4 | R$ 0,50 | R$ 2,00 |
| **LEDs Extras (Painel Indicador)** | 3 | R$ 0,20 | R$ 0,60 |
| **Resistores (220Ω ou 330Ω)** | 3 | R$ 0,10 | R$ 0,30 |
| **Buzzer Ativo (3.3V/5V)** | 1 | R$ 5,00 | R$ 5,00 |
| **Protoboard e Jumpers** | 1 | R$ 15,00 | R$ 15,00 |
| **Subtotal Estimado** | - | - | **~ R$ 237,90** |

### 3.4 Tecnologias usadas
* **Sistema Operacional:** Linux (Raspberry Pi OS)
* **Serviços:** Mosquitto MQTT Broker
* **Interface Visual:** Python (PyQt/Tkinter) OU Servidor Web com ASP.NET Core MVC / Flask
* **Integração de Hardware:** Python com biblioteca `gpiozero` ou `RPi.GPIO`
* **Dashboard Cloud:** Dojo Toolkit (JavaScript/HTML/CSS)

---

## 4. Parte 3: O Nó Secundário (ESP8266)

### 4.1 O ESP8266 (Repeteco do primeiro)
Expandir a rede replicando a arquitetura de leitura e controle do ESP32 em um microcontrolador mais simples.

### 4.2 Descrição do que a parte faz
Funciona exatamente como a Parte 1. Controla um segundo grupo de 3 LEDs, monitora a queima deles via transistores NPN e lê a luminosidade de outro ponto do ambiente usando seu único pino analógico disponível (A0). Conecta-se ao Wi-Fi e se reporta ao Raspberry Pi.

### 4.3 Componentes usados e preços

| Componente | Quantidade | Preço Unitário Médio | Preço Total Estimado |
| :--- | :---: | :--- | :--- |
| **Placa ESP8266 (NodeMCU)** *(Já adquirido)*| 1 | R$ 30,00 | R$ 30,00 |
| **LEDs (5mm)** | 3 | R$ 0,20 | R$ 0,60 |
| **Resistores (220Ω ou 330Ω)** | 3 | R$ 0,10 | R$ 0,30 |
| **Transistores NPN (BC548)** | 3 | R$ 0,30 | R$ 0,90 |
| **Módulo Sensor de Luz LDR (com LM393)** | 1 | R$ 7,00 | R$ 7,00 |
| **Protoboard e Jumpers** | 1 | R$ 15,00 | R$ 15,00 |
| **Subtotal Estimado** | - | - | **~ R$ 53,80** |

### 4.4 Tecnologias usadas
* **Linguagem:** C/C++
* **Ambiente:** Arduino IDE
* **Bibliotecas:** `ESP8266WiFi.h`, `PubSubClient.h` (para MQTT)

---

## 5. Lista de Todos os Componentes Usados e Preços

| Componente | Quantidade | Função no Projeto | Preço Unitário Médio | Preço Total Estimado |
| :--- | :---: | :--- | :--- | :--- |
| **Raspberry Pi Zero W** | 1 | Servidor central e painel de controle físico. | R$ 180,00 | R$ 180,00 |
| **Placa ESP32 (NodeMCU)** | 1 | Nó principal (Lê LEDs, controla e envia dados). | R$ 45,00 | R$ 45,00 |
| **Placa ESP8266 (NodeMCU)** | 1 | Nó secundário (Lê LEDs, controla e envia dados). | R$ 30,00 | R$ 30,00 |
| **Cartão MicroSD (Classe 10)**| 1 | Armazenar o sistema operacional do Raspberry Pi. | R$ 35,00 | R$ 35,00 |
| **LEDs (5mm Diversos)** | 9 | 3 para o ESP32, 3 para o ESP8266, 3 para o painel do Pi. | R$ 0,20 | R$ 1,80 |
| **Resistores (330Ω ou 220Ω)** | 9 | Limitar corrente dos 9 LEDs do projeto. | R$ 0,10 | R$ 0,90 |
| **Transistores NPN (BC548)** | 6 | Sensores para detectar se os LEDs dos ESPs queimaram. | R$ 0,30 | R$ 1,80 |
| **Módulo Sensor de Luz (LDR)**| 2 | Medir a luminosidade ambiente (1 no ESP32, 1 no ESP8266).| R$ 7,00 | R$ 14,00 |
| **Botões Push Button** | 4 | Controles físicos para o painel do Raspberry Pi. | R$ 0,50 | R$ 2,00 |
| **Buzzer Ativo (3.3V/5V)** | 1 | Alerta sonoro no Raspberry Pi para LEDs queimados. | R$ 5,00 | R$ 5,00 |
| **Protoboards** | 3 | Montagem dos circuitos sem necessidade de solda inicial. | R$ 15,00 | R$ 45,00 |
| **Kit Jumpers (Fios)** | 1 | Conectar os componentes nas protoboards. | R$ 20,00 | R$ 20,00 |
| **Custo Total Estimado** | - | - | - | **~ R$ 380,50** |

---

## 6. Todas as Tecnologias Usadas no Projeto
* **Hardware:** ESP32, ESP8266, Raspberry Pi Zero W, Sensores e Atuadores discretos.
* **Comunicação:** Wi-Fi, Protocolo MQTT (Eclipse Mosquitto).
* **Firmware (Nós):** C/C++ na plataforma Arduino IDE.
* **Backend / Lógica Local:** Python (com bibliotecas de manipulação de GPIO). Opção de uso de C# (ASP.NET Core MVC) para o servidor web embarcado.
* **Frontend / Dashboard Cloud:** Dojo Toolkit, HTML5, CSS3, JavaScript.

### Pinouts das Placas

---

#### *ESP32:*
<div align="center">
  <img src="https://www.upesy.com/cdn/shop/files/doc-esp32-pinout-reference-wroom-devkit.png" alt="Pinout ESP32" width="800">
</div>

> *Fonte: https://www.upesy.com/blogs/tutorials/esp32-pinout-reference-gpio-pins-ultimate-guide*

---

#### *ESP8266:*
<div align="center">
  <img src="https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2019/05/ESP8266-NodeMCU-kit-12-E-pinout-gpio-pin.png?resize=817%2C542&quality=100&strip=all&ssl=1" alt="Pinout ESP8266" width="800">
</div>

> *Fonte: https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/*

#### *Raspberry Pi Zero W*
<div align="center">
  <img src="https://images.wevolver.com/eyJidWNrZXQiOiJ3ZXZvbHZlci1wcm9qZWN0LWltYWdlcyIsImtleSI6ImZyb2FsYS8xNzY1MTYwNDM1NzQyLTE3NjUxNjA0MzU3NDIucG5nIiwiZWRpdHMiOnsicmVzaXplIjp7IndpZHRoIjo5NTAsImZpdCI6ImNvdmVyIn19fQ==" alt="Pinout Raspberry Pi Zero W" width="800">
</div>

> *Fonte: https://www.wevolver.com/article/raspberry-pi-zero-2-w-pinout-comprehensive-guide-for-engineers*

---

## 7. Esquema Eletrônico

<div align="center">
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQeJQeJyzgAzTEVqXiGe90RGBFhfp_4RcJJMQ&s" alt="Esquema Eletrônico do Sistema IoT" width="400">
</div>
*Figura 1: Representação do esquema de ligações dos microcontroladores, transistores de detecção de queima, sensores LDR e painel de controle físico. (Inserir diagrama elétrico final aqui).*
