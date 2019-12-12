#NEED TO HAVE THE SQLITE ACCESS THE VERY LAST ENTRY
from flask import Flask, request, render_template
import RPi.GPIO as GPIO
import sqlite3
import time
import datetime
import random
import _thread
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.IN)
GPIO.setup(6,GPIO.IN)
GPIO.setup(13,GPIO.IN)
GPIO.setup(19,GPIO.IN)
GPIO.setup(26,GPIO.IN)
#need to confirm that its in html folder, but rest of the path is correcct
#need to install apache, as it does not have the deisred folder 
def read():
    f=open('/var/www/html/2bit.txt',"w")
    five=GPIO.input(5)
    four=GPIO.input(6)
    three=GPIO.input(13)
    two=GPIO.input(19)
    one=GPIO.input(26)
    if five:
        print("Vin equals 5 volts")
        f.write("Vin equals 5 volts")
    elif four:
        print("Vin equals 4 volts")
        f.write("Vin equals 4 volts")
    elif three:
        print("Vin equals 3 volts")
        f.write("Vin equals 3 volts")
    elif two:
        print("Vin equals 2 volts")
        f.write("Vin equals 2 volts")
    elif one:
        print("Vin equals 1 volts")
        f.write("Vin equals 1 volts")
    else:
        print("Vin equals 0 volts")
        f.write("Vin equals 0 volts")
    f.close()
while True:
    read()
    time.sleep(10)
