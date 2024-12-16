import machine
import time
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep
from machine import deepsleep
import json
import network
import urequests
import os
from ota import OTAUpdater

# Función para conectar a la red WiFi
def conectar_wifi(ssid, contraseña):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Conectando a la red '{ssid}'...")
        wlan.connect(ssid, contraseña)
        start_time = time.time()


        while not wlan.isconnected():
            if time.time() - start_time > 10:
                print("No se pudo conectar a la red WiFi.")
                return None
            time.sleep(1)


    print("Conexión exitosa!")
    print("Datos de conexión (IP/netmask/gw/DNS):", wlan.ifconfig())
    return wlan

# Función para obtener la dirección MAC del ESP32
def obtener_mac(wlan):
    mac = wlan.config('mac')
    mac_str = ':'.join(f'{b:02X}' for b in mac)
    print(f"Dirección MAC: {mac_str}")
    return mac_str

def obtener_ip():
    ip = wlan.ifconfig()[0]
    return ip

# Función para configurar el cliente MQTT
def configurar_mqtt(mqtt_server, mqtt_port, client_id):
    client = MQTTClient(client_id, mqtt_server, port=int(mqtt_port))
    try:
        client.connect()
        print("Conectado al servidor MQTT")
    except Exception as e:
        print(f"Error al conectar al servidor MQTT: {e}")
        return None
    return client

# Función para enviar datos por MQTT en formato JSON
def enviar_datos_mqtt(client, topic, mac, ip, estado):
    data = {
        "Identificador": "esp32-pruebas",
        "IP": ip,
        "Estado": estado
    }
    json_data = json.dumps(data)
    client.publish(topic, json_data)
    print(f"Datos enviados: {json_data}")

# Función para enviar correo electrónico
def enviar_correo_con_reintento(remitente, contrasena, destinatario, asunto, mensaje, intentos=10):
    for intento in range(intentos):
        try:
            smtp = SMTP('smtp.gmail.com', 465, ssl=True)
            smtp.login(remitente, contrasena)
            smtp.to(destinatario)
            smtp.write(f"Subject: {asunto}\n")
            smtp.write(f"{mensaje}\n")
            smtp.send()
            smtp.quit()
            print("Correo enviado con éxito!")
            return True
        except Exception as e:
            print(f"Error al enviar el correo (intento {intento + 1} de {intentos}): {e}")
            if intento < intentos - 1:
                print("Reintentando en 5 segundos...")
                time.sleep(5)
    print("No se pudo enviar el correo después de varios intentos.")
    return False

# Configurar deep sleep con RTC para despertar después de un tiempo
def entrar_en_deep_sleep(tiempo_ms):
    print(f"Entrando en deep sleep por {tiempo_ms / 1000} segundos...")
    machine.deepsleep(tiempo_ms)

def detectar_sleep():
# Detectar si el ESP32 está despertando de deep sleep
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print("Despertando del modo deep sleep.")
    else:
        print("Inicio desde un reinicio o encendido.")

def ota_isaza():
# Inicializar el OTA Updater
#    firmware_url = "https://raw.githubusercontent.com/juan-Angel32/OTA/main/"
#    filename = "prueba ota.py"
    ota_updater = OTAUpdater(ssid, contraseña_wifi, firmware_url, filename)

# Procesos principales
def ejecutar_procesos():
    red = conectar_wifi(ssid, contraseña_wifi)
    if red:
        mac_str = obtener_mac(red)
        ip = red.ifconfig()[0]

        client = configurar_mqtt(MQTT_SERVER, MQTT_PORT, MQTT_CLIENT_ID)
        if client:
            enviar_datos_mqtt(client, MQTT_TOPIC, mac_str, ip, estado)

            mensaje_correo = f"El dispositivo con MAC '{mac_str}' sigue en línea. Su IP es {ip}."
            enviar_correo_con_reintento(correo_remitente, contrasena_remitente, correo_destinatario, asunto, mensaje_correo)

        # Desconectar WiFi para ahorrar energía
        red.active(False)

    # Entrar en deep sleep por 1 minuto
    entrar_en_deep_sleep(tiempo_deep_sleep)



# %%%%%%%%% MAIN BLUCLE    %%%%%%%%%%%%%%%%%%%%
#ejecutar_procesos()
wlan = conectar_wifi(ssid, contraseña_wifi)
MAC=obtener_mac(wlan)
IP=obtener_ip()

while True:
    ota_isaza()
    time.sleep(5)
    print("Ciclo Update from Github Version 2")
    #configurar_mqtt(MQTT_SERVER, MQTT_PORT, MQTT_CLIENT_ID)
    #enviar_datos_mqtt(client,MQTT_TOPIC, MAC, IP, estado)
    #entrar_en_deep_sleep(tiempo_deep_sleep)
    #machiene.reset()
    
    





#import Blink_Led

#import ssd1306
#i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
#oled = ssd1306.SSD1306_I2C(128, 64, i2c)
#
#### Define pins
#led = Pin(2, Pin.OUT)
#### Definition of the Client, Broker, and Client to Publish information
#CLIENT_NAME = 'Thing1'
#BROKER_ADDR = '62.146.181.199'
#TOPIC = CLIENT_NAME.encode() + b'/sw'
#BTN_TOPIC = CLIENT_NAME.encode() + b'/Sensor3'
#mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
#mqttc.connect()

#Variable1 = 'X'

#def sub_cb(topic,msg):
#    if msg.decode()=='1':
#        print('UNO')
#        led.value(1)
#    if msg.decode()=='0':
#        print('ZERO')
#        led.value(0)

#X=2

#with open('config.json', 'r') as f:
#    print('leyendo inicial')
#    config = json.load(f)
#    print(config['X'])
#    print('se leyo e imprmio X')
#    X = config['X']
    #X=int(X)
#    print('Lectura_Inicial de')
#    print(X)

#while True:
#    oled.poweron()
#    oled.fill(0)
#    oled.text('TecSIoT', 0, 0)
#    oled.text('Thing1/Sensor3', 0, 9)
#    oled.text(str(X).encode(), 0, 19)
#    oled.text('62.146.181.199', 0, 28)
#    oled.text('INFINITUMD930_2.4', 0, 37)
#    oled.text('Dr. Cesar Isaza', 0, 48)
#    oled.text('July 2024', 0, 57)
#    oled.show()
     
    # Received values from dashboard switch
#    mqttc.set_callback(sub_cb)
#    mqttc.subscribe(TOPIC)
#    mqttc.check_msg()
    
    # Publish X values to dashboard
#    mqttc.subscribe(BTN_TOPIC)
#    mqttc.publish(BTN_TOPIC, str(X).encode())
#    X = int(X)
#    X = X+1
    
#    sleep(60)
#    oled.poweroff()
    
#    config = {
#        Variable1: str(X).encode(),
#    }
#    with open('config.json', 'w') as f:
#        json.dump(config, f)
#    print('Before Deepsleep',X)
#    deepsleep(60000) 


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# SSID = 'WorkStation1'
# PASSWORD = 'tacho11056'
# #URL = "https://github.com/cesarisaza/ESP32_OTA/blob/main/main.py"
# URL = "https://raw.githubusercontent.com/cesarisaza/ESP32_OTA/refs/heads/main/Blink_Led.py"
# 
# def connect_to_wifi():
#     wlan = network.WLAN(network.STA_IF)
#     wlan.active(True)
#     wlan.connect(SSID,PASSWORD)
#     
#     print("Connecting to WIFI......", end="")
#     for i in range(5):
#         if wlan.isconnected():
#             print("\nWIFI Connected")
#             return True
#         print(".",end="")
#         time.sleep(1)
#         
#     print("\n Can´t Connect to WIFI.")
#     return False
# 
# def download_and_run():
#     try:
#         print("Downloading the latest version of Blink_Led.py desde TECSIOT-Github")
#         response = urequests.get(URL)
#         if response.status_code==200:
#             print("Successfully Blink_Led.py downloaded.")
#             with open('Blink_Led.py','w') as f:
#                 f.write(response.text)
#             print("Blink_Led.py update succesfully")
#             
#             import Blink_Led
#         else:
#             print("Error downloading the file, state code:", response.status_code)
#     except Exception as e:
#         print("OTA Error updating",e)
#         
#     
# if connect_to_wifi():
#     download_and_run()
# else:
#     print("WIFI Problems so Error Updating main.py")
# #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    
    
