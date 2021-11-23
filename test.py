import RPi.GPIO as GPIO
import time



GPIO.setmode(GPIO.BOARD)

counter1 = 37

GPIO.setup(counter1, GPIO.IN)
# GPIO.setup(counter1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


try:  
    while True : 
        print (GPIO.input(counter1)) 
        time.sleep(0.02)
except:
    GPIO.cleanup() 

# seamer 8
# counter1 = 37
# GPIO.setup(counter1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# counter2 = 33
# GPIO.setup(counter2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# seamer 7
# counter2 = 37
# GPIO.setup(counter1, GPIO.IN)