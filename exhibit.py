from pscb import PSCB
import config
import time
try:
    import RPi.GPIO as GPIO
    DEVICE_MODE = 'pi'
except Exception as e:
    DEVICE_MODE = 'test'
    from EmulatorGUI import GPIO

# THIS IS THE MAIN SCRIPT TO RUN THE PSCB EXHIBIT

if __name__ == '__main__':
    try:
        #app = PSCB()
        #app.main()

        #app.test_input()
        GPIO.setmode(GPIO.BCM)
        while True:
            GPIO.output(config.PWR_TRAIN, 1)
            time.sleep(1)
            GPIO.output(config.PWR_TRAIN, 0)
            time.sleep(1)


    except KeyboardInterrupt:
        # handle ctrl-c
        print("keyboard stop")


    except Exception as e:
        # other exceptions
        print(e)
        print("closing")

    finally:
        GPIO.cleanup()
