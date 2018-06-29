from pscb import PSCB
import config
import time

try:
    import RPi.GPIO as GPIO
    DEVICE_MODE = 'pi'
except Exception as e:
    DEVICE_MODE = 'test'
    from EmulatorGUI import GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

app = PSCB()
app.init_pins()

for pin in config.PIN_GROUP_OUTPUT:
    GPIO.output(pin, GPIO.LOW)

while True:
    time.sleep(50)
