from pscb import PSCB
import config
import time
import os
try:
    import RPi.GPIO as GPIO
    DEVICE_MODE = 'pi'
except Exception as e:
    DEVICE_MODE = 'test'
    from EmulatorGUI import GPIO


def write_crash(type, text):
    if not os.path.isdir(config.CRASH_PATH):
        os.mkdir(config.CRASH_PATH)

    with open(config.CRASH_PATH+type+'_'+str(time.time())+'.txt', 'w') as out:
        out.write(str(text))


# THIS IS THE MAIN SCRIPT TO RUN THE PSCB EXHIBIT
if __name__ == '__main__':
    try:
        app = PSCB()

        app.start_exhibit()
        if DEVICE_MODE == 'pi':
            app.init_input()


    except KeyboardInterrupt:
        # handle ctrl-c
        print("keyboard stop")
        write_crash('keyboard_interrupt', 'keyboard stop')


    except Exception as e:
        # other exceptions
        write_crash('keyboard_interrupt', e)
        print(e)
        print("closing")

    finally:
        try:
            GPIO.cleanup()
        except:
            print("GPIO Clean Up failed")
            # ignore, if we can clean up there is nothing we can do
