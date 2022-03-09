import paho.mqtt.client as mqtt
import time

def log_on_log(client,userdata,level,buf):
    print(f'Log> {buf}')

def check_on_connect(client,userdata,flags,rc):
    if rc == 0:
        print('OK')
    else:
        print(f'Bad connect >>> {rc}')

def on_disconnect(client,userdata,flags,rc=0):
    print(f'Desconectado! Código>> {str(rc)} ')

def on_message(client,userdata,msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8","ignore"))
    print(f'Mensagem Recebida >> {m_decode}')

broker = 'test.mosquitto.org'
client = mqtt.Client('emcimaembaixo')

client.on_connect = check_on_connect
client.on_log =  log_on_log #é possivel desativar o logger simplesmente comentando a linha inteira que define a função
client.on_disconnect = on_disconnect
client.on_message = on_message

print(f'conectando à {broker}')

client.connect(broker)
client.loop_start()
client.subscribe("freioDaBlze")
client.publish("freioDaBlze","hoje ela quer tar do lado") # tópico, mensagem

time.sleep(3)
client.loop_stop() 
client.disconnect()
print(f'{broker} finished')