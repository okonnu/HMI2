import RPi.GPIO as GPIO
import time



GPIO.setmode(GPIO.BOARD)

counter1 = 33

GPIO.setup(counter1, GPIO.IN)
# GPIO.setup(counter1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


try:  
    while True : 
        print (GPIO.input(counter1)) 
        time.sleep(0.05)
except:
    GPIO.cleanup() 
