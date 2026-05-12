import json
import tkinter as tk
from tkinter import ttk, messagebox
import paho.mqtt.client as mqtt

# --- MOCK PARA WINDOWS ---
from gpiozero.pins.mock import MockFactory
from gpiozero import Device, LED, Button, Buzzer
Device.pin_factory = MockFactory()

# --- CONFIGURAÇÃO HARDWARE ---
led_aviso_1, led_aviso_2, led_aviso_3 = LED(4), LED(27), LED(22)
buzzer = Buzzer(18)
btn_pins = [5, 6, 13, 26]
btns = [Button(p, pull_up=True, bounce_time=0.1) for p in btn_pins]

# --- CONFIGURAÇÃO MQTT ---
BROKER = "broker.emqx.io"
TOPIC_SUB = "cidade/bairros/status"
TOPIC_PUB = "cidade/bairros/comandos"

class AppInterface:
    def __init__(self, root, mqtt_client):
        self.root = root
        self.root.title("SmartCity Dashboard v2.1")
        self.root.geometry("900x600")
        self.root.configure(bg="#0f172a") 
        
        self.mqtt_client = mqtt_client
        self.bairros_data = {} 
        self.bairros_lista = []
        self.bairro_selecionado_idx = -1
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#0f172a")
        self.style.configure("TLabel", background="#0f172a", foreground="#f8fafc")

        # Cabeçalho com Legenda de Cores
        header = tk.Frame(root, bg="#1e293b", height=80)
        header.pack(fill=tk.X)
        tk.Label(header, text="MONITORAMENTO URBANO", font=("Urbanist", 18, "bold"), bg="#1e293b", fg="#38bdf8").pack(pady=(15, 0))
        
        # Legenda
        legenda = tk.Frame(header, bg="#1e293b")
        legenda.pack(pady=5)
        self._add_legenda(legenda, "🟢 Ligado", "#22c55e")
        self._add_legenda(legenda, "⚫ Desligado", "#475569")
        self._add_legenda(legenda, "🔴 Queimado", "#ef4444")

        # Painel Lateral
        sidebar = tk.Frame(root, bg="#1e293b", width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        tk.Label(sidebar, text="COMANDOS", font=("Arial", 10, "bold"), bg="#1e293b", fg="#94a3b8").pack(pady=(20,10))
        
        self.btn_select = self._create_nav_btn(sidebar, "TROCAR BAIRRO", self.selecionar_proximo_bairro, "#38bdf8")
        self._create_nav_btn(sidebar, "LIGAR LUZES", lambda: self.enviar_comando("ligar_manual"), "#22c55e")
        self._create_nav_btn(sidebar, "DESLIGAR LUZES", lambda: self.enviar_comando("desligar_manual"), "#ef4444")
        self._create_nav_btn(sidebar, "RESET SISTEMA", lambda: self.enviar_comando("resetar_sistema"), "#fbbf24")

        self.lbl_selected = tk.Label(sidebar, text="Nenhum Selecionado", font=("Arial", 9, "bold"), bg="#1e293b", fg="#ec4899")
        self.lbl_selected.pack(pady=20)

        # Área Principal
        self.main_area = tk.Frame(root, bg="#0f172a")
        self.main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _add_legenda(self, parent, texto, cor):
        tk.Label(parent, text=texto, fg=cor, bg="#1e293b", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=10)

    def _create_nav_btn(self, parent, text, cmd, color):
        b = tk.Button(parent, text=text, command=cmd, bg="#334155", fg=color, font=("Arial", 9, "bold"), 
                      relief=tk.FLAT, bd=0, height=2, cursor="hand2", activebackground="#475569")
        b.pack(fill=tk.X, padx=15, pady=5)
        return b

    def processar_msg(self, payload):
        try:
            # Estrutura JSON recebida
            dados = json.loads(payload)
            bairro = dados[1]
            
            if bairro not in self.bairros_data:
                self.bairros_lista.append(bairro)
                self.root.after(0, self._criar_card_bairro, bairro)
            
            self.root.after(0, self._atualizar_card, dados)
            self._atualizar_hardware_aviso(dados[3:]) # Manda a fatia com os 3 objs dos LEDs
            
        except Exception as e: 
            print(f"Erro JSON: {e}")

    def _criar_card_bairro(self, nome):
        frame = tk.Frame(self.main_area, bg="#1e293b", bd=2, relief=tk.FLAT, padx=15, pady=15)
        frame.pack(fill=tk.X, pady=5)
        
        lbl_nome = tk.Label(frame, text=nome.upper(), font=("Arial", 12, "bold"), bg="#1e293b", fg="#f8fafc")
        lbl_nome.pack(side=tk.LEFT)

        info_frame = tk.Frame(frame, bg="#1e293b")
        info_frame.pack(side=tk.RIGHT)

        lbl_lum = tk.Label(info_frame, text="Lum: --%", bg="#1e293b", fg="#94a3b8", font=("Arial", 10, "bold"))
        lbl_lum.pack(side=tk.LEFT, padx=20)

        # Canvas para as luzes
        canvas = tk.Canvas(info_frame, width=100, height=30, bg="#1e293b", highlightthickness=0)
        canvas.pack(side=tk.LEFT)
        leds_shapes = [canvas.create_oval(5+i*30, 5, 25+i*30, 25, fill="#334155") for i in range(3)]

        self.bairros_data[nome] = {"frame": frame, "lbl_lum": lbl_lum, "canvas": canvas, "leds": leds_shapes}

    def _atualizar_card(self, dados):
        _, nome, lum, l1, l2, l3 = dados
        card = self.bairros_data[nome]
        card["lbl_lum"].config(text=f"LUMINOSIDADE: {lum}%")
        
        status_luzes = [l1["Status"], l2["Status"], l3["Status"]]
        
        for i in range(3):
            # Identifica a cor baseada na string de status
            if status_luzes[i] == "Ligado":
                color = "#22c55e"    # Verde
            elif status_luzes[i] == "Desligado":
                color = "#475569"    # Cinza Escuro
            elif status_luzes[i] == "Queimado":
                color = "#ef4444"    # Vermelho Neon
            else:
                color = "#334155"    # Cor de fallback
                
            card["canvas"].itemconfig(card["leds"][i], fill=color)

    def selecionar_proximo_bairro(self):
        if not self.bairros_lista: return
        
        if self.bairro_selecionado_idx != -1:
            prev = self.bairros_lista[self.bairro_selecionado_idx]
            self.bairros_data[prev]["frame"].config(highlightbackground="#1e293b", highlightthickness=2)

        self.bairro_selecionado_idx = (self.bairro_selecionado_idx + 1) % len(self.bairros_lista)
        atual = self.bairros_lista[self.bairro_selecionado_idx]
        
        self.bairros_data[atual]["frame"].config(highlightbackground="#38bdf8", highlightthickness=2)
        self.lbl_selected.config(text=f"BAIRRO ALVO:\n{atual}")

    def enviar_comando(self, acao):
        if self.bairro_selecionado_idx == -1:
            messagebox.showwarning("Aviso", "Selecione um bairro usando o botão físico 4 ou na interface!")
            return
        
        bairro = self.bairros_lista[self.bairro_selecionado_idx]
        payload = json.dumps({"acao": acao, "bairro": bairro})
        self.mqtt_client.publish(TOPIC_PUB, payload)
        print(f"Comando enviado: {payload}")

    def _atualizar_hardware_aviso(self, status_leds):
        # A contagem de falhas (hardware) agora só é ativada se a string for "Queimado"
        falhas = sum(1 for led in status_leds if led["Status"] == "Queimado")
        
        led_aviso_1.value = (falhas >= 1)
        led_aviso_2.value = (falhas >= 2)
        led_aviso_3.value = (falhas == 3)
        
        if falhas == 3: buzzer.on()
        else: buzzer.off()
        
        if falhas > 0:
            print(f"[HW ALERTA] Falhas reais: {falhas} lâmpadas queimadas | Buzzer: {'ON' if falhas==3 else 'OFF'}")

# --- MQTT CALLBACKS ---
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0: client.subscribe(TOPIC_SUB)

def on_message(client, userdata, msg):
    if userdata and "app" in userdata:
        userdata["app"].processar_msg(msg.payload.decode())

# --- EXECUÇÃO ---
if __name__ == "__main__":
    mqtt_ud = {}
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=mqtt_ud)
    client.on_connect, client.on_message = on_connect, on_message
    client.connect(BROKER, 1883, 60)
    client.loop_start()

    root = tk.Tk()
    app = AppInterface(root, client)
    mqtt_ud["app"] = app

    btns[0].when_pressed = app.selecionar_proximo_bairro
    btns[1].when_pressed = lambda: app.enviar_comando("ligar_manual")
    btns[2].when_pressed = lambda: app.enviar_comando("desligar_manual")
    btns[3].when_pressed = lambda: app.enviar_comando("resetar_sistema")

    root.mainloop()