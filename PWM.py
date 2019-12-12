import RPi.GPIO as GPIO          
import time                            
GPIO.setwarnings(False)           
GPIO.setmode (GPIO.BCM)         
GPIO.setup(19,GPIO.OUT)
x=512
p = GPIO.PWM(19,512)          
p.start(50)
for i in range(100000000):
    x=512 + sin(512)
    
