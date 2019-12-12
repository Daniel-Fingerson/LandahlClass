import spidev
import time
spi = spidev.SpiDev()
spi.max_speed_hz = 5000
while True:
    time.sleep(.1)
    spi.open(0, 0)
    to_send = [0x01]
    spi.xfer(to_send)
    spi.close()
