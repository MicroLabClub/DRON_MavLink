import paho.mqtt.client as mqtt
import pymysql.cursors
import json
import common_utils
from datetime import datetime
from time import sleep

# MQTT credentials
username = 'sergiu.doncila'
password = 'QWEasd!@#123'
host = '9b7b323ee67e46d18f9317162c8e8841.s1.eu.hivemq.cloud'
port = 8883

# Connect to MySQL
connection = pymysql.connect(host='mysql-utm-platform-db-microlab-agro-platform.a.aivencloud.com',
                             user='avnadmin',
                             password='AVNS_2bInbWIclqi_tBITcbF',
                             database='utm-platform',
                             port=17613,
                             cursorclass=pymysql.cursors.DictCursor)

def insert_message(topic, message, table_name):
    json_message = json.loads(message)
    device_id = json_message['device_id'] 
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        with connection.cursor() as cursor:
            sql = f"INSERT INTO {table_name} (`device_id`, `topic`, `message`, `date`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (device_id, topic, message, date))
            connection.commit()
            print(f"Message added: {cursor.lastrowid}")
    except Exception as e:
        print(f"Error on SQL insert message: {e}")

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Publisher connected to MQTT")
    client.subscribe('microlab/automotive/#')

def on_message(client, userdata, msg):
    print(f"Received message on topic: {msg.topic}")
    message_str = msg.payload.decode('utf-8')
    print(f"Message to string: {message_str}")

    table_name = "messages_mqqt"

    if msg.topic == "microlab/automotive/device/drone/battery":
        print("Settings topic")
        print(message_str)

        # Process your received message here, if needed

    else:
        insert_message(msg.topic, message_str, table_name)

def insert_message(topic, message, table_name):
    json_message = json.loads(message)
    device_id = json_message['device_id']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        with connection.cursor() as cursor:
            sql = f"INSERT INTO {table_name} (`device_id`, `topic`, `message`, `date`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (device_id, topic, message, date))
            connection.commit()
            print(f"Message added: {cursor.lastrowid}")
    except Exception as e:
        print(f"Error on SQL insert message: {e}")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT")

def connect_mqtt_client():
    client = mqtt.Client()
    return client

def run_mqtt_publisher(client, vehicle):
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.tls_set()

    client.connect(host, port)
    client.loop_start()
    battery_time = 10
    set_battery_interval(battery_time, client, vehicle)

def set_battery_interval(battery_time, client, vehicle):
    while True:
        client.publish('microlab/automotive/device/drone/battery-1', json.dumps({'battery': common_utils.get_battery_value(vehicle), 'device_id': 2}))
        client.publish('microlab/automotive/device/drone/coord-1', json.dumps({'coordinates': common_utils.get_coordinates(vehicle), 'device_id': 2}))
        sleep(battery_time)
