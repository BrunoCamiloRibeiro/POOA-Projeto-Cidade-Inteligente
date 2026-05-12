import json
import tkinter as tk # A biblioteca padrão do Python para criar interfaces gráficas
from tkinter import ttk, messagebox # ttk é para estilos mais modernos, messagebox para pop-ups de aviso
import paho.mqtt.client as mqtt
from gpiozero import LED, Button, Buzzer # Importação REAL para os pinos físicos do Raspberry

# ==========================================
# 1. CONFIGURAÇÃO DO HARDWARE FÍSICO
# ==========================================
led_aviso_1 = LED(4)
led_aviso_2 = LED(27)
led_aviso_3 = LED(22)
buzzer = Buzzer(18)

# Botões configurados com resistores de pull-up internos
# bounce_time=0.1 evita que o botão conte vários cliques se o contato físico "tremer"
btn_pins = [5, 6, 13, 26]
btns = [Button(p, pull_up=True, bounce_time=0.1) for p in btn_pins]

# ==========================================
# 2. CONFIGURAÇÃO MQTT
# ==========================================
BROKER = "broker.emqx.io"
TOPIC_SUB = "cidade/bairros/status"
TOPIC_PUB = "cidade/bairros/comandos"

# ==========================================
# 3. INTERFACE GRÁFICA (A Classe Principal)
# ==========================================
class AppInterface:
    def __init__(self, root, mqtt_client):
        # O 'root' é a janela principal da sua aplicação (A base de tudo)
        self.root = root
        self.root.title("SmartCity Dashboard v2.1")
        self.root.geometry("900x600") # Largura x Altura da janela
        self.root.configure(bg="#0f172a") # Cor de fundo (Background)
        
        self.mqtt_client = mqtt_client
        self.bairros_data = {} 
        self.bairros_lista = []
        self.bairro_selecionado_idx = -1
        
        # Configurando um estilo global para coisas que usam ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#0f172a")
        
        # --- CABEÇALHO ---
        # tk.Frame é como uma div no HTML. Serve para agrupar elementos.
        header = tk.Frame(root, bg="#1e293b", height=80)
        # O comando .pack() "joga" o elemento na tela. 
        # fill=tk.X faz ele preencher todo o espaço horizontal.
        header.pack(fill=tk.X) 
        
        # tk.Label é apenas um texto estático na tela.
        tk.Label(header, text="MONITORAMENTO URBANO", font=("Urbanist", 18, "bold"), bg="#1e293b", fg="#38bdf8").pack(pady=(15, 0))
        
        legenda = tk.Frame(header, bg="#1e293b")
        legenda.pack(pady=5)
        self._add_legenda(legenda, "🟢 Ligado", "#22c55e")
        self._add_legenda(legenda, "⚫ Desligado", "#475569")
        self._add_legenda(legenda, "🔴 Queimado", "#ef4444")

        # --- PAINEL LATERAL (SIDEBAR) ---
        sidebar = tk.Frame(root, bg="#1e293b", width=250)
        # side=tk.LEFT empurra esse bloco para o lado esquerdo da tela. fill=tk.Y faz ele preencher a altura.
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5) 
        
        tk.Label(sidebar, text="COMANDOS", font=("Arial", 10, "bold"), bg="#1e293b", fg="#94a3b8").pack(pady=(20,10))
        
        # Criando os botões da interface que simulam os botões físicos
        self.btn_select = self._create_nav_btn(sidebar, "TROCAR BAIRRO", self.selecionar_proximo_bairro, "#38bdf8")
        self._create_nav_btn(sidebar, "LIGAR LUZES", lambda: self.enviar_comando("ligar_manual"), "#22c55e")
        self._create_nav_btn(sidebar, "DESLIGAR LUZES", lambda: self.enviar_comando("desligar_manual"), "#ef4444")
        self._create_nav_btn(sidebar, "RESET SISTEMA", lambda: self.enviar_comando("resetar_sistema"), "#fbbf24")

        self.lbl_selected = tk.Label(sidebar, text="Nenhum Selecionado", font=("Arial", 9, "bold"), bg="#1e293b", fg="#ec4899")
        self.lbl_selected.pack(pady=20)

        # --- ÁREA PRINCIPAL (Onde os bairros vão aparecer) ---
        self.main_area = tk.Frame(root, bg="#0f172a")
        # expand=True diz para esse frame roubar todo o espaço que sobrou na janela
        self.main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # --- FUNÇÕES DE DESENHO DA INTERFACE ---
    def _add_legenda(self, parent, texto, cor):
        tk.Label(parent, text=texto, fg=cor, bg="#1e293b", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=10)

    def _create_nav_btn(self, parent, text, cmd, color):
        # tk.Button é um botão clicável. 'command=cmd' diz qual função rodar quando for clicado.
        b = tk.Button(parent, text=text, command=cmd, bg="#334155", fg=color, font=("Arial", 9, "bold"), 
                      relief=tk.FLAT, bd=0, height=2, cursor="hand2", activebackground="#475569")
        b.pack(fill=tk.X, padx=15, pady=5)
        return b

    # --- LÓGICA DE NEGÓCIO ---
    def processar_msg(self, payload):
        try:
            dados = json.loads(payload)
            bairro = dados[1]
            
            # Se o bairro ainda não existe na nossa tela, vamos criar o card dele
            if bairro not in self.bairros_data:
                self.bairros_lista.append(bairro)
                # IMPORTANTE: root.after(0, ...) serve para atualizar a interface gráfica de forma segura.
                # Como o MQTT roda em "segundo plano" (outra thread), ele não pode mexer na tela diretamente.
                self.root.after(0, self._criar_card_bairro, bairro)
            
            self.root.after(0, self._atualizar_card, dados)
            self._atualizar_hardware_aviso(dados[3:]) 
            
        except Exception as e: 
            print(f"Erro JSON: {e}")

    def _criar_card_bairro(self, nome):
        # Cria a "caixa" visual para o novo bairro
        frame = tk.Frame(self.main_area, bg="#1e293b", bd=2, relief=tk.FLAT, padx=15, pady=15)
        frame.pack(fill=tk.X, pady=5)
        
        lbl_nome = tk.Label(frame, text=nome.upper(), font=("Arial", 12, "bold"), bg="#1e293b", fg="#f8fafc")
        lbl_nome.pack(side=tk.LEFT)

        info_frame = tk.Frame(frame, bg="#1e293b")
        info_frame.pack(side=tk.RIGHT)

        lbl_lum = tk.Label(info_frame, text="Lum: --%", bg="#1e293b", fg="#94a3b8", font=("Arial", 10, "bold"))
        lbl_lum.pack(side=tk.LEFT, padx=20)

        # tk.Canvas é uma área livre para desenhar. Usamos para fazer os "LEDs redondos" da interface.
        canvas = tk.Canvas(info_frame, width=100, height=30, bg="#1e293b", highlightthickness=0)
        canvas.pack(side=tk.LEFT)
        
        # Desenhando 3 círculos (ovals)
        leds_shapes = [canvas.create_oval(5+i*30, 5, 25+i*30, 25, fill="#334155") for i in range(3)]

        # Salvamos tudo num dicionário para conseguir alterar depois (quando chegar nova mensagem)
        self.bairros_data[nome] = {"frame": frame, "lbl_lum": lbl_lum, "canvas": canvas, "leds": leds_shapes}

    def _atualizar_card(self, dados):
        _, nome, lum, l1, l2, l3 = dados
        card = self.bairros_data[nome]
        
        # Atualiza o texto da luminosidade usando .config()
        card["lbl_lum"].config(text=f"LUMINOSIDADE: {lum}%")
        
        status_luzes = [l1["Status"], l2["Status"], l3["Status"]]
        
        for i in range(3):
            # Lógica para mudar a cor dos círculos no Canvas dependendo da string recebida
            if status_luzes[i] == "Ligado":
                color = "#22c55e"    # Verde
            elif status_luzes[i] == "Desligado":
                color = "#475569"    # Cinza Escuro
            elif status_luzes[i] == "Queimado":
                color = "#ef4444"    # Vermelho Neon
            else:
                color = "#334155"    # Cor padrão
                
            # itemconfig serve para alterar propriedades de um desenho no canvas
            card["canvas"].itemconfig(card["leds"][i], fill=color)

    def selecionar_proximo_bairro(self):
        if not self.bairros_lista: return
        
        # Remove a borda colorida do bairro selecionado anteriormente
        if self.bairro_selecionado_idx != -1:
            prev = self.bairros_lista[self.bairro_selecionado_idx]
            self.bairros_data[prev]["frame"].config(highlightbackground="#1e293b", highlightthickness=2)

        # Avança para o próximo bairro da lista (Volta a 0 se chegar no final)
        self.bairro_selecionado_idx = (self.bairro_selecionado_idx + 1) % len(self.bairros_lista)
        atual = self.bairros_lista[self.bairro_selecionado_idx]
        
        # Coloca a borda azul neon no bairro atual selecionado
        self.bairros_data[atual]["frame"].config(highlightbackground="#38bdf8", highlightthickness=2)
        self.lbl_selected.config(text=f"BAIRRO ALVO:\n{atual}")

    def enviar_comando(self, acao):
        if self.bairro_selecionado_idx == -1:
            # Mostra um pop-up de erro se tentar enviar comando sem selecionar o bairro antes
            messagebox.showwarning("Aviso", "Selecione um bairro usando o botão físico 4 ou na interface!")
            return
        
        bairro = self.bairros_lista[self.bairro_selecionado_idx]
        payload = json.dumps({"acao": acao, "bairro": bairro})
        self.mqtt_client.publish(TOPIC_PUB, payload)
        print(f"Comando enviado: {payload}")

    def _atualizar_hardware_aviso(self, status_leds):
        # Conta quantas strings "Queimado" existem na mensagem que chegou
        falhas = sum(1 for led in status_leds if led["Status"] == "Queimado")
        
        # Liga (True) ou desliga (False) os LEDs físicos reais
        led_aviso_1.value = (falhas >= 1)
        led_aviso_2.value = (falhas >= 2)
        led_aviso_3.value = (falhas == 3)
        
        # Liga o buzzer físico se houver 3 falhas
        if falhas == 3: buzzer.on()
        else: buzzer.off()

# ==========================================
# 4. FUNÇÕES DE CALLBACK DO MQTT
# ==========================================
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0: 
        print("Conectado ao Broker!")
        client.subscribe(TOPIC_SUB)

def on_message(client, userdata, msg):
    # Repassa a mensagem recebida para a nossa Interface Processar
    if userdata and "app" in userdata:
        userdata["app"].processar_msg(msg.payload.decode())

# ==========================================
# 5. INICIALIZAÇÃO DO PROGRAMA
# ==========================================
if __name__ == "__main__":
    mqtt_ud = {}
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=mqtt_ud)
    client.on_connect = on_connect
    client.on_message = on_message
    
    # Inicia a conexão MQTT
    client.connect(BROKER, 1883, 60)
    client.loop_start()

    # Cria a janela principal do Tkinter
    root = tk.Tk()
    app = AppInterface(root, client)
    mqtt_ud["app"] = app # Salva a interface no MQTT para podermos atualizar a tela quando chegar mensagem

    # Aqui é onde a mágica do hardware acontece:
    # Vinculamos o evento 'when_pressed' (quando pressionado) dos botões físicos às funções da interface.
    btns[0].when_pressed = app.selecionar_proximo_bairro
    btns[1].when_pressed = lambda: app.enviar_comando("ligar_manual")
    btns[2].when_pressed = lambda: app.enviar_comando("desligar_manual")
    btns[3].when_pressed = lambda: app.enviar_comando("resetar_sistema")

    # Isso impede o programa de fechar. Fica aguardando cliques e mensagens infinitamente.
    root.mainloop()