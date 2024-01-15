#!/usr/bin/python
import sys
import time
import json
import threading
import common_utils
from dronekit import connect, VehicleMode
from publisher import run_mqtt_publisher, connect_mqtt_client
from subscriber import run_mqtt_subscriber, connect_mqtt_client2

connection_string = '/dev/serial0'
sys_tick = 5
stop_collection_flag = False

def connect_vehicle():
    print("Connecting to vehicle on port: %s" % (connection_string,))
    vehicle = connect(connection_string, baud=115200)
    return vehicle

def collect_data(vehicle):

    global stop_collection_flag
    while not stop_collection_flag:
        print("Get data from vehicle:")
        print("\t GPS: %s" % vehicle.gps_0)
        print("\t Battery: %s" % vehicle.battery.level)
        print("\t Latitude: %s" % vehicle.location.global_relative_frame.lat)
        print("\t Longitude: %s" % vehicle.location.global_relative_frame.lon)
        print("\t Altitude: %s" % vehicle.location.global_relative_frame.alt)
        time.sleep(sys_tick)

    print("Stopped data collection.")

    vehicle.close()

def stop_collection():
    global stop_collection_flag
    stop_collection_flag = True

if __name__ == "__main__":
    vehicle = connect_vehicle()

    if vehicle:
        mqtt_client = connect_mqtt_client()  # Aici se face conexiunea MQTT
        mqtt_client2 = connect_mqtt_client2()
        if mqtt_client:
            data_collection_thread = threading.Thread(target=collect_data, args=(vehicle,))
            mqtt_publisher_thread = threading.Thread(target=run_mqtt_publisher, args=(mqtt_client, vehicle,))
            mqtt_subscriber_thread = threading.Thread(target=run_mqtt_subscriber, args=(mqtt_client2)) 

            data_collection_thread.start()
            mqtt_publisher_thread.start()
            mqtt_subscriber_thread.start()
        else:
            print("Failed to connect to MQTT. Exiting.")
            sys.exit(1)  # Ieșirea din program cu codul de ieșire 1
    else:
        print("No vehicle connection. Exiting.")
        sys.exit(1)  # Ieșirea din program cu codul de ieșire 1
