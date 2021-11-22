
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BOARD)  
  
pinn = 33
# GPIO pinn set up as input. It is pulled up to stop false signals  
GPIO.setup(pinn, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
  
print ("Waiting for falling edge on port pinn")
try:  
    GPIO.wait_for_edge(pinn, GPIO.FALLING)   
    print ("interrupt detected" ) 
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()