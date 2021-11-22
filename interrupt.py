
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BOARD)  
  
pinn = 33
# GPIO pinn set up as input. It is pulled up to stop false signals  
GPIO.setup(pinn, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
  
print ("Make sure you have a button connected so that when pressed" ) 
print ("it will connect GPIO port pinn (pin 16) to GND (pin 6)\n")  
raw_input("Press Enter when ready\n>")  
  
print ("Waiting for falling edge on port pinn"  
# now the program will do nothing until the signal on port pinn   
# starts to fall towards zero. This is why we used the pullup  
# to keep the signal high and prevent a false interrupt  
  
print "During this waiting time, your computer is not"   
print "wasting resources by polling for a button press.\n"  
print "Press your button when ready to initiate a falling edge interrupt."  
try:  
    GPIO.wait_for_edge(pinn, GPIO.FALLING)  
    print "\nFalling edge detected. Now your program can continue with"  
    print "whatever was waiting for a button press."  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()