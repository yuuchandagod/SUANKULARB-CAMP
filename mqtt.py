from ast import Return
from multiprocessing.connection import Client
import paho.mqtt.client as mqtt
import os
import time
import paho.mqtt.client as mqtt
# Define event callbacks


def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))


def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(client, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(client, obj, level, string):
    print(string)
# setup mqtt client call backs


def initClient(usr: str, pwd: str):
    mqttc = mqtt.Client()
    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    # Uncomment to enable debug messages
    mqttc.on_log = on_log
    # Connect
    mqttc.username_pw_set(usr, pwd)  # made up username and password
    # mqttc.connect(url.hostname, url.port) # establish connection
    mqttc.connect("cansat.info", 1883)
    print('connecting')
    mqttc.loop_start()
    return mqttc


def disconnectClient(mqttc: mqtt.Client):
    mqttc.disconnect()


def sendserver(mqttc: mqtt.Client, data: str):
    # Publish a message
    print('sending mqtt')
    mqttc.publish('teams/1072', data)  # send the line of data


def test(mqttc):
    idx = 1
    t = 1
    C = f'1072,10:44:35:208,{idx},C,F,0,0.65,26.76,13.19,0:00:00,14.9943,03.1039,0,0,PRELAUNCH,CXON'
    T = f'1072,3:04:18,{idx},T,45.16,25.34,7.5,-0.06,0.06,0.06,-0.38,1.46,9.77,0.12,0.25,0.19,12,ACQUIRING_TARGET'
    while True:
        try:
            C = f'1072,10:44:35:208,{idx},C,F,0,0.65,26.76,13.19,0:00:00,14.9943,03.1039,0,0,PRELAUNCH,CXON'
            T = f'1072,3:04:18,{idx},T,5.16,25.34,7.5,-0.06,0.06,0.06,-0.38,1.46,9.77,0.12,0.25,0.19,12,ACQUIRING_TARGET'
            time.sleep(t)
            mqttc.publish('teams/1072', C)  # send the line of data
            print(C)
            time.sleep(t)
            mqttc.publish('teams/1072', T)  # send the line of data
            print(T)
            time.sleep(t)
            idx += 1

            print("pingsen")
        except KeyboardInterrupt:
            disconnectClient(mqttc)
            break


if __name__ == "__main__":
    mqttc = initClient("1072", "Cyygkiqi171")
    test(mqttc)
