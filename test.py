import RPi.GPIO as GPIO
import datetime



GPIO.setmode(GPIO.BOARD)

counter1 = 33

# GPIO.setup(counter1, GPIO.IN)
GPIO.setup(counter1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


try:  
    while True : 
        print (GPIO.input(counter1)) 
except:
    GPIO.cleanup() 
