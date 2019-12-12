#written by Daniel Fingerson
import spidev
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def read():
    raw_adc=[0,0,0,0]
    voltages=[0,0,0,0]
    spi2=spidev.SpiDev()
    spi2.open(0,0)
    spi2.max_speed_hz=1350000
    buf=[[ 0x01, 0x00, 0x00],[ 0x01, 0x20, 0x00],[ 0x01, 0x40, 0x00],[ 0x01, 0x60, 0x00]]
    spi2.xfer2(buf[0])
    raw_adc=((buf[0][1] &3)<<8) +buf[0][2] #bitwise shift operation to only read the 10 desired bits
    voltage=(raw_adc*5)/1023 #ADCres code to voltage conversion
    return voltage
    '''
    for i in range(4):
        raw_adc[i]=((buf[i][1] &3)<<8) +buf[i][2] #converts last 10 bits of data into an ADC reading
        voltages[i]=(raw_adc[i]*5)/1023 #converts ADC reading into a voltage
        #print("Ch {} - Ch{}:".format(i,i+1))
        #print('{0:.3f} volts'.format( voltages[i]))#prints voltages to 3 decimal place
    '''
    spi2.close()
    return voltage

def ry():
    voltage=read

