import digitalio
import board
import time
import usb_hid
import neopixel
import rotaryio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

#Funzione controllo della matrice tasti
def CheckMatrix():
    for maggio in range(len(ROW)):
        ROW[maggio].value=True
        led.fill((0,0,0))
        for tello in range(len(COL)):
            led.fill((0,0,0))
            if COL[tello].value==True:
                led.fill((0,255,0))
                kbd.send(MAP[maggio][tello])
                while COL[tello].value==True:
                    time.sleep(0.001)

        ROW[maggio].value=False

led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness=0.3
led.fill((0,0,0))

#Led configurato sui pin D2 e D1
encoder = rotaryio.IncrementalEncoder(board.D2, board.D1)

last_position = 0

#Dichiarazione righe
ROW = [
    board.D3, board.D9, board.D7
]

for chetta in range(len(ROW)):
    ROW[chetta]=digitalio.DigitalInOut(ROW[chetta])
    ROW[chetta].direction = digitalio.Direction.OUTPUT

#Dichiarazione colonne
COL =[
    board.D0, board.D4, board.D5, board.D6
]

for tello in range(len(COL)):
    COL[tello] = digitalio.DigitalInOut(COL[tello])
    COL[tello].switch_to_input(pull=digitalio.Pull.DOWN)


#KEYMAP
kbd = Keyboard(usb_hid.devices)

MAP = [[Keycode.F13, Keycode.F14, Keycode.F15, Keycode.F16],
       [Keycode.F17, Keycode.F18, Keycode.F19, Keycode.F20],
       [Keycode.F21, Keycode.F22, Keycode.F23, Keycode.F24]]

while True:
    led.fill((0,0,0))
    CheckMatrix()
    current_position = encoder.position

    if current_position != last_position:
        if current_position > last_position:
            # Rotazione Oraria -> Blu
            kbd.send(Keycode.SHIFT, Keycode.F1)
            led.fill((0, 0, 255))
            print("Rotazione Oraria (+)")
        else:
            # Rotazione Antioraria -> Giallo
            kbd.send(Keycode.CONTROL, Keycode.F1)
            led.fill((255, 255, 0))
            print("Rotazione Antioraria (-)")

        last_position = current_position

        # Aspetta un attimo e spegni il LED per evidenziare lo scatto
        time.sleep(0.05)
        led.fill((0, 0, 0))



