from webbrowser import Chrome
import paho.mqtt.client as mqtt
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import random
from turtle import Screen




chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
driver = webdriver.Chrome(chrome_options=chrome_options)

stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
    )

m_decode = 0
aux_dec = 0
luz_ligada = False


def log_on_log(client,userdata,level,buf):
    print(f'Log> {buf}')

def on_connect(client,userdata,flags,rc):
    if rc == 0:
        print('OK')
    else:
        print(f'Bad connect >>> {rc}')

def on_disconnect(client,userdata,flags,rc=0):
    print(f'Desconectado! Código>> {str(rc)} ')

def on_message(client,userdata,msg):
    global m_decode
    global aux_dec

    if msg.topic == "home/ligaluz":
        m_decode = str(msg.payload.decode("utf-8","ignore"))
    elif msg.topic == "home/selenium":
        aux_dec = str(msg.payload.decode("utf-8","ignore"))



broker = "test.mosquitto.org"

client = mqtt.Client("Main")
client.connect(broker)


client.on_connect = on_connect
#client.on_log =  log_on_log é possivel desativar o logger simplesmente comentando a linha inteira que define a função
client.on_disconnect = on_disconnect
client.on_message = on_message


client.loop_start()
client.subscribe("home/ligaluz")
client.subscribe("home/selenium")

music_play = False

while True:
    time.sleep(.1)
    print(m_decode)
    if aux_dec == '1':
        if not music_play:
            music_play = True
            driver = webdriver.Chrome()
            driver.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=1s")
    if m_decode == 0:
        continue
    elif m_decode == "1":
        if luz_ligada != False:
            continue
        else:
            print("liga")
            screen= Screen()
            screen.bgcolor("White")
            luz_ligada = True
    elif m_decode == '2':      
        if luz_ligada != True:
            continue
        else:  
            print("desliga")
            screen=Screen()
            screen.bye()
            luz_ligada = False
            
