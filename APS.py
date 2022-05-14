from turtle import Screen
import os
import psutil
import time
from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as publish



def on_message_lb(mosq, obj, msg):
    if msg.payload.decode()=="1":
        print("liga")
        screen= Screen()
        screen.bgcolor("White")
    if msg.payload.decode()=="0":
        print("desliga")
        screen=Screen()
        screen.bye()

def on_message_yt(mosq, obj, msg):
    if msg.payload.decode()!="":
        print (msg.payload.decode())

def on_message_active_resources(mosq, obj, msg):
    msg=msg.payload.decode()
    print(msg)
    if msg=="1":
        msgMemory = psutil.virtual_memory()[2]
        publish.single("APSCC2022/MEMusage", msgMemory, hostname="test.mosquitto.org")
        print (msgMemory)
        msgCpu = psutil.cpu_percent(4)
        publish.single("APSCC2022/CPUsage", msgCpu, hostname="test.mosquitto.org")
    if msg=="0":
        publish.single("APSCC2022/CPUsage", msg, hostname="test.mosquitto.org")
        publish.single("APSCC2022/MEMusage", msg, hostname="test.mosquitto.org")
         
        
# def on_message_cpu(mosq, obj, msg):
#     global active
#     
#     while msgCpu==msgCpu:
#         repete()
#         def repete():
#             msgCpu = psutil.cpu_percent(4)
#             publicar.single("APSCC2022/CPUsage", msgCpu, hostname="test.mosquitto.org")
#             print (msgCpu)

           
# def on_message(mosq, obj, msg):
#     print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

mqtt = mqtt_client.Client()

mqtt.message_callback_add('APSCC2022/youtube', on_message_yt)
mqtt.message_callback_add('APSCC2022/lightBulb', on_message_lb)
mqtt.message_callback_add('APSCC2022/resources', on_message_active_resources)
# mqtt.on_message = on_message
mqtt.connect("test.mosquitto.org", 1883, 30)
mqtt.subscribe("APSCC2022/#")

mqtt.loop_forever()