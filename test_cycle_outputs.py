from pscb import PSCB
import config
import time

try:
    import RPi.GPIO as GPIO
    DEVICE_MODE = 'pi'
except Exception as e:
    DEVICE_MODE = 'test'
    from EmulatorGUI import GPIO

sleep_time = 3
app = PSCB('test_cycle_outputs.py')
while True:
    app.mode_set(0)
    print("running train")
    app.run_train()
    time.sleep(sleep_time)
    app.output_reset()

    print("running crossing")
    app.run_crossing()
    time.sleep(sleep_time)
    app.output_reset()

    print("running signal")
    app.run_signal()
    time.sleep(sleep_time)
    app.output_reset()

    print("running crosswalk")
    app.run_crosswalk()
    time.sleep(sleep_time)
    app.output_reset()

    print("running eme")
    app.run_eme()
    time.sleep(10)
    app.output_reset()

    app.mode_set(1)

    print("running train")
    app.run_train()
    time.sleep(sleep_time)
    app.output_reset()
    print("running crossing")
    app.run_crossing()
    time.sleep(sleep_time)
    app.output_reset()

    print("running signal")
    app.run_signal()
    time.sleep(sleep_time)
    app.output_reset()

    print("running crosswalk")
    app.run_crosswalk()
    time.sleep(sleep_time)
    app.output_reset()

    print("running eme")
    app.run_eme()