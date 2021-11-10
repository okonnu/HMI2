import eel
import random
import time
from paho.mqtt import client as mqtt_client
import threading
import datetime
import RPi.GPIO as GPIO
import sys

eel.init('web')

canspercase = 24
team = 'group1'
target = 150
shift = 'shift1'

broker = '192.168.1.247'
port = 1883
topic = "test"
client_id = 'C4'
username = 'dmkl'
password = 'delmo'

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

counter1 = 37
previous1 = False
cnt1 = 0

counter2 = 33
previous2 = False
cnt2 = 0
cont2 = 0
downtime = 0
pr2 = 0
cspeed = 0
eque = []
eff = 0
damages = 0
delay = 0 

now = datetime.datetime.now()

GPIO.setup(counter1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(counter2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

@eel.expose
def set_pyconfigs(jclient_id, jteam, jcanspercase, jtarget):
    client_id = jclient_id
    team = jteam
    canspercase = jcanspercase
    target = int(jtarget)
    shift = getshift()
    print("running js from pythonn")
    eel.set_jsconfigs(client_id, team, canspercase, target, shift)
    print(getshift())
set_pyconfigs('C4', "GROUP A", "24", "200")
 
def countcans1():
   global cnt1, previous1, counter1
   threading.Timer(0.10, countcans1).start()
   if GPIO.input(counter1) == 1 and previous1 == False:
       cnt1 = cnt1 + 1
       print("counter1 : " + str(cnt1))
       previous1 = True
   elif GPIO.input(counter1) == 0 and previous1 == True:
       previous1 = False
       
def countcans2():
    global cnt1,cnt2, previous2, counter2, delay, downtime
    threading.Timer(0.10, countcans2).start()
    delay = delay + 0.10
    if GPIO.input(counter2) == 1 and previous2 == False:
        cnt2 = cnt2 + 1
        print("counter2 : " + str(cnt2))
        downtime = downtime + delay
        delay = 0
        previous2 = True
    elif GPIO.input(counter2) == 0 and previous2 == True:
        previous2 = False
        # set values to js
    damages = cnt1-cnt2    
    eel.set_metrics(cnt2, round(cnt2/canspercase,1), damages, round(downtime/60, 2))
    
def getshift():
    if int(now.hour) in (6,7,8,9,10,11,12,13):
        return 'shift1'
    if  int(now.hour)  in (14,15,16,17,18,19,20,21):
        return 'shift2'
    if  int(now.hour)  in (22,23,0,1,2,3,4,5) :
        return 'shift3'
    


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
client = connect_mqtt()

def publish():
    global cnt1, cnt2, cont2, downtime
    msg = '{"clientID":"'+ str(client_id) +'","cans":" ' + str(cnt2) + '","cases":"' + str(round(cnt2/canspercase,1)) + '","cspeed":"'+ str(cspeed * 60) +'","tstamp":"1385816","downtime":"'+str(downtime)+'"}'
    topic = 'test'
    result = client.publish(topic, msg)
    status = result[0]
    if status != 0:
        print(str(status) + "Failed to send message to topic")
        
    
def sendcans():
    global cnt2, downtime, pr2, cspeed, canspercase
    threading.Timer(1.0, sendcans).start()
    cspeed = cnt2 - pr2
    pr2 = cnt2
    eque.append(cspeed)
    if len(eque) < 5 :
        eque.append(cspeed)
    else :
        eque.pop(0)
    eff = round((sum(eque)*12 / target)*100, 1)
    eel.set_eff(eff)
    publish()

sendcans()
countcans1()
countcans2()
eel.start('index.html', host='localhost', port=27000, size=(800, 480), position=(0,0), )
