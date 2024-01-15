import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO  # Importul pentru controlul pinului GPIO pe Raspberry Pi
import json
import time

# MQTT credentials
username = 'sergiu.doncila'  
password = 'QWEasd!@#123'  
host = '9b7b323ee67e46d18f9317162c8e8841.s1.eu.hivemq.cloud'  
port = 8883  

def on_connect(client, userdata, flags, rc):
    print("Subscriber connected to MQTT")
    client.subscribe('microlab/automotive/device/drone/startMission-1')  # Abonare la topicul de interes

def on_message(client, userdata, msg):
    print(f"Received message on topic: {msg.topic}")
    payload = msg.payload.decode('utf-8')
    print(f"Message received: {payload}")

    # Procesează mesajul primit aici conform nevoilor tale

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT")

def run_mqtt_subscriber(client):
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.tls_set()
    client.connect(host, port)
    client.loop_forever()  # Păstrează conexiunea deschisă și ascultă mesajele în buclă


led_pin = 18

# Inițializarea pinului GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.LOW)  # Pornim LED-ul inițial stins

# Funcția pentru a controla LED-ul pe baza mesajelor MQTT primite
def on_message(client, userdata, msg):
    print(f"Received message on topic: {msg.topic}")
    payload = msg.payload.decode('utf-8')
    print(f"Message received: {payload}")

    # Procesează mesajul primit aici conform nevoilor tale
    if msg.topic == 'microlab/automotive/device/drone/startMission-1':
        GPIO.output(led_pin, GPIO.HIGH)  # Aprinde LED-ul
        print("Mission received! LED turned ON.")

        for _ in range(5):
            GPIO.output(led_pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(led_pin, GPIO.LOW)
            time.sleep(1)
        # Aici poți adăuga și alte acțiuni în funcție de mesajul primit

# Restul codului pentru subscriber rămâne neschimbat

# ... (restul codului din subscriber)

def connect_mqtt_client2():
    client = mqtt.Client()
    return client

if __name__ == "__main__":
    client = connect_mqtt_client2()
    run_mqtt_subscriber(client)
