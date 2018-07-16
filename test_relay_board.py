from pscb import PSCB
import config
import time

try:
    import RPi.GPIO as GPIO
    DEVICE_MODE = 'pi'
except Exception as e:
    DEVICE_MODE = 'test'
    from EmulatorGUI import GPIO

app = PSCB('test_relay_board.py')
c = 0
while c != 16:
    try:
        GPIO.setup((config.PIN_RELAY_BOARD_START + c), GPIO.OUT)
    except:
        # this likely its already setup
        donothing = 1
    c += 1

while True:
    c = 0
    while c != 16:
        GPIO.output((config.PIN_RELAY_BOARD_START+c), GPIO.LOW)
        c += 1
    time.sleep(2)
    c = 0
    while c != 16:
        GPIO.output((config.PIN_RELAY_BOARD_START+c), GPIO.HIGH)
        c += 1
    time.sleep(2)