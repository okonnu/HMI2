import RPi.GPIO as GPIO
import datetime



GPIO.setmode(GPIO.BOARD)

counter1 = 37

GPIO.setup(counter1, GPIO.IN)


try:  
    while True : 
        print (GPIO.input(counter1)) 
except:
    GPIO.cleanup() 
