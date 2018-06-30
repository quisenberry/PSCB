from pscb import PSCB
import config
import time

try:
    import RPi.GPIO as GPIO
    DEVICE_MODE = 'pi'
except Exception as e:
    DEVICE_MODE = 'test'
    from EmulatorGUI import GPIO


def press(pin):
    print("pressed: "+str(pin))


if DEVICE_MODE == 'test':
    print("This script will only work directly on a Pi")
    exit(1)
else:
    app = PSCB()
    for pin in config.PIN_GROUP_INPUT:
        GPIO.add_event_detect(pin, GPIO.FALLING, press)

    try:
        while True:
            time.sleep(60)

    except KeyboardInterrupt:
        # handle ctrl-c
        print("keyboard stop")
        GPIO.cleanup()


    except Exception as e:
        # other exceptions
        GPIO.cleanup()
        print(e)
        print("closing")

    finally:
        GPIO.cleanup()

