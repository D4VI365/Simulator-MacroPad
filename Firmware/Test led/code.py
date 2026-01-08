import digitalio
import board
import time

led = digitalio.DigitalInOut(board.D10)
led.direction=digitalio.direction.OUTPUT

while 1:
    led.value=True
    time.sleep(500)
    led.value=False
    time.sleep(500)