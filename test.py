
import RPi.GPIO as GPIO
import time
import os
from dotenv import load_dotenv

GPIO.setmode(GPIO.BOARD)

testpin = os.getenv('TEST_PIN')


if (os.getenv('TEST_PIN') == "UP"):
    print("setting testpin on pull-up mode")
    GPIO.setup(testpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
elif (os.getenv('TEST_PIN') == "DOWN"):
    print("setting testpin on pull-down mode")
    GPIO.setup(testpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
else:
    print("setting testpin on plain mode")
    GPIO.setup(testpin, GPIO.IN)
    
    
def handle(pin):
    print ("interrupt fired")) 
    
    
GPIO.add_event_detect(BTN_B, GPIO.FALLING, lambda pin: GPIO.output(LED_B, True))

try:  
    while True : 
        print (GPIO.input(testpin)) 
        time.sleep(0.02)
except:
    GPIO.cleanup() 

# seamer 8
# testpin = 37
# GPIO.setup(testpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# counter2 = 33
# GPIO.setup(counter2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# seamer 7
# counter2 = 37
# GPIO.setup(testpin, GPIO.IN)