import eel
import random
import time
from paho.mqtt import client as mqtt
import threading
import datetime
import RPi.GPIO as GPIO
import sys
import os
from dotenv import load_dotenv
from resetRpi import restart

eel.init('web')
load_dotenv()

canspercase = int(os.getenv('CANSPERCASE'))
team = 'group1'
target = int(os.getenv('TARGET_PER_MIN'))
shift = 'shift1'

broker = os.getenv('MQTT_SERVER')
port = os.getenv('MQTT_PORT')
topic = os.getenv('DATA_TOPIC')
client_id = os.getenv('CLIENT_ID')
username = os.getenv('MQTT_USER')
password = os.getenv('MQTT_PASS')

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

counter1 = int(os.getenv('COUNTER1_PIN'))
previous1 = False
cnt1 = 0

counter2 = int(os.getenv('COUNTER2_PIN'))
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

def setpinmode(PIN, pinmode):
    if (pinmode == "UP"):
        print("setting pin " + str(PIN) + " on pull-up mode")
        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    elif (pinmode == "DOWN"):
        print("setting pin " + str(PIN) + " on pull-down mode")
        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    else:
        print("setting PIN " + str(PIN) + " on plain mode")
        GPIO.setup(PIN, GPIO.IN)

setpinmode(counter1, os.getenv('COUNTER1_MODE') )
setpinmode(counter2, os.getenv('COUNTER2_MODE') )

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
 
def countcans1():
    global cnt1, previous1, counter1
    threading.Timer(0.05, countcans1).start()
    if GPIO.input(counter1) == 1 and previous1 == False:
        cnt1 = cnt1 + 1
        print("counter1 : " + str(cnt1))
        previous1 = True
    elif GPIO.input(counter1) == 0 and previous1 == True:
        previous1 = False
    damages = cnt1-cnt2  
       
def countcans2():
    global cnt1,cnt2, previous2, counter2, delay, downtime
    threading.Timer(0.05, countcans2).start()
    delay = delay + 0.05
    if GPIO.input(counter2) == 1 and previous2 == False:
        cnt2 = cnt2 + 1
        print("counter2 : " + str(cnt2))
        downtime = downtime + delay
        delay = 0
        previous2 = True
    elif GPIO.input(counter2) == 0 and previous2 == True:
        previous2 = False
        # set values to js  
    eel.set_metrics(cnt2, round(cnt2/canspercase,1), damages, round(downtime/60, 2))
    
def getshift():
    if int(now.hour) in (6,7,8,9,10,11,12,13):
        return 'shift1'
    if  int(now.hour)  in (14,15,16,17,18,19,20,21):
        return 'shift2'
    if  int(now.hour)  in (22,23,0,1,2,3,4,5) :
        return 'shift3'
    


def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe(os.getenv('DATA_TOPIC'))  # Subscribe to the topic “digitest/test1”, receive any messages published on it
    client.subscribe(os.getenv('RESET_TOPIC'))

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    # print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    if msg.topic == os.getenv('RESET_TOPIC'):
        print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
        restart()

client = mqtt.Client(os.getenv('CLIENT_ID'))  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
username = os.getenv('MQTT_USER')
password = os.getenv('MQTT_PASS')
client.username_pw_set(username, password)
print(os.getenv('MQTT_PORT'))
client.connect(os.getenv('MQTT_SERVER'))
client.loop_start()  #Start loop


def publish():
    global cnt1, cnt2, cont2, downtime, damages
    msg = '{"clientID":"'+ str(client_id) +'","cans":" ' + str(cnt2) + '","cases":"' + str(round(cnt2/canspercase,1)) + '","cspeed":"'+ str(cspeed * 60) +'","tstamp":"'+str(time.time()) +'","damages":"'+str(damages)+'","downtime":"'+str(downtime)+'"}'
    topic = os.getenv('DATA_TOPIC')
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


set_pyconfigs(client_id, "GROUP A", "24", "200")
sendcans()

if os.getenv('COUNTER1_STATUS') == "ENABLED":
    countcans1()
if os.getenv('COUNTER2_STATUS') == "ENABLED":
    countcans2()

eel.start('index.html', host='localhost', port=27011, size=(1280,960), position=(0,0), cmdline_args=['--incognito','--disable-infobars','--start-fullscreen'] )
