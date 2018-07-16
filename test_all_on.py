from pscb import PSCB
import config
import time

try:
    import RPi.GPIO as GPIO
    DEVICE_MODE = 'pi'
except Exception as e:
    DEVICE_MODE = 'test'
    from EmulatorGUI import GPIO

app = PSCB('test_all_on.py')

for pin in config.PIN_GROUP_OUTPUT:
    GPIO.output(pin, GPIO.LOW)

while True:
    time.sleep(50)
