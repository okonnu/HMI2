import eel
import random
import time
from paho.mqtt import client as mqtt_client
import threading
import datetime
import RPi.GPIO as GPIO

eel.init('web')

broker = '192.168.1.247'
port = 1883
topic = "cookroom"
client_id = 'c6'
username = 'dmkl'
password = 'delmo'

canspercase = 24
team = 'group1'
target = '150'
shift = 'shift1'

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

counter1 = 33
previous1 = False
cnt1 = 0

counter2 = 37
previous2 = False
cnt2 = 0
cont2 = 0
downtime = 0
pr2 = 0
cspeed = 0
eque = []
eff = 0
damages = 0

now = datetime.datetime.now()

GPIO.setup(counter1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(counter2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

@eel.expose
def set_pyconfigs(configs):
    client_id = configs[0]
    team = configs[1]
    canspercase = configs[2]
    target = configs[3]
    shift = getshift()
    eel.set_jsconfigs(client_id, team, canspercase, target, shift)
 
def countcans():
    global cnt1, cnt2, previous1, previous2, counter1, counter2
    threading.Timer(0.05, countcans).start()
        # time.sleep(0.03)
        # if GPIO.input(counter1) == 1 and previous1 == False:
        #     cnt1 = cnt1 + 1
        #     print("counter1 : " + str(cnt1))
        #     previous1 = Truesendcans
        # elif GPIO.input(counter1) == 0 and previous1 == True:
        #     previous1 = False


    if GPIO.input(counter2) == 1 and previous2 == False:
        cnt2 = cnt2 + 1
        print("counter2 : " + str(cnt2))
        previous2 = True
    elif GPIO.input(counter2) == 0 and previous2 == True:
        previous2 = False
        # set values to js
        eel.set_metrics(cnt2, cnt2/canspercase, damages, downtime, eff)
    
def getshift():
    if int(now.hour) > 5 and  int(now.hour)  < 14:
        return 'shift1'
    if  int(now.hour)  > 13 and  int(now.hour)  < 22:
        return 'shift2'
    if  int(now.hour)  > 21 and  int(now.hour)  < 6 : 
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
    msg = '{"clientID":"'+ str(client_id) +'","cans":" ' + str(cnt2) + '","cases":"' + str(cnt2/canspercase) + '","cspeed":"'+ str(cspeed * 60) +'","tstamp":"1385816","downtime":"'+str(downtime)+'"}'
    topic = 'cookroom'
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print (msg)
    else:
        print("Failed to send message to topic")
        
    
def sendcans():
    global cnt2, downtime, pr2, cspeed, canspercase
    threading.Timer(1.0, sendcans).start()
    cspeed = cnt2 - pr2
    pr2 = cnt2
    print (cnt2)
    if len(eque) < 5 :
        eque.append(cspeed)
    else :
        eque.pop()
    eff = round(sum(eque)*12 / canspercase, 1)
    
    publish()

sendcans()
countcans()
eel.start('index.html', host='localhost', port=27000, size=(700, 480), position=(0,0), )