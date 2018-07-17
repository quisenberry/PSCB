import config
import wave
import pyaudio
import time
import sys
import threading
import pygame
import os
import datetime

try:
    import RPi.GPIO as GPIO
    DEVICE_MODE = 'pi'
except Exception as e:
    DEVICE_MODE = 'test'
    from EmulatorGUI import GPIO

AUDIO_MODE = 'pygame'


class PSCB:
    sound = False
    mode = 0
    mode_press_state = False
    mode_sequence_current = 0
    sequence_timeout = 0
    last_press_time = 0
    sequence = [
        config.INPUT_TRAIN,
        config.INPUT_CROSSING,
        config.INPUT_SIGNAL,
        config.INPUT_CROSSWALK,
        config.INPUT_EME
    ], [
        config.INPUT_EME,
        config.INPUT_SIGNAL,
        config.INPUT_TRAIN,
        config.INPUT_CROSSING
    ]
    mode_step = 0
    last_press = 0
    press_lock = False

    def __init__(self, starting_with='None'):
        self.log('')
        self.log('### Starting Exhibit ###')
        self.log('')
        self.log('starting with: '+str(starting_with))
        # INIT GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # INIT PINS
        self.init_pins()


    def start_exhibit(self):
        self.mode_set(2)

        # INIT INPUT (not supported in EmulatorGUI)
        if DEVICE_MODE == 'pi':
            self.init_input()

        # TEST AUDIO
        #self.test_audio()

        # INIT MODE BUTTON (Mode is polled) nothing can be called after this
        self.monitor_mode_btn()

    def init_pins(self):
        for pin in config.PIN_GROUP_INPUT:
            self.log("setting pin "+str(pin)+" as input")
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        for pin in config.PIN_GROUP_OUTPUT:
            self.log("setting pin "+str(pin)+" as output")
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)

    def init_input(self):
        for pin in config.PIN_GROUP_INPUT:
            GPIO.add_event_detect(pin, GPIO.FALLING, self.press)

    def test_output_pins(self):
        # CYCLE ON EACH RELAY ONE AT A TIME
        for pin in config.PIN_GROUP_OUTPUT:
            self.log("testing output pin: "+str(pin))
            GPIO.output(pin, GPIO.LOW)
            time.sleep(1)
            GPIO.output(pin, GPIO.HIGH)

        time.sleep(1)

    def monitor_mode_btn(self):
        while True:
            while GPIO.input(config.INPUT_MODE) == GPIO.HIGH:
                time.sleep(0.01)
                # used to check for a press
                if self.last_press_time:
                    if time.time() > (self.last_press_time + config.RESET_TIMEOUT):
                        self.log("timeout")
                        self.log(self.last_press_time)
                        self.output_reset()
                        self.mode_set(2)

            self.log("mode button pressed")
            self.mode_toggle()
            while GPIO.input(config.INPUT_MODE) == GPIO.LOW:
                time.sleep(0.01)

    def play(self, wave_file):
        t = threading.Thread(target=self.play_wav, args=(wave_file,))
        t.daemon = True
        t.start()

    def play_wav(self, wav_filename, chunk_size=1024):

        if AUDIO_MODE == 'pygame':
            pygame.mixer.init()
            pygame.init()


            # load the sound file
            mysound = pygame.mixer.Sound(wav_filename)

            # play the sound file for 15 seconds max and then stop it
            mysound.play()
            time.sleep(8)
            pygame.mixer.music.fadeout(2)
            mysound.stop()
        else:
            '''
            Play (on the attached system sound device) the WAV file
            named wav_filename.
            '''
            try:
                try:
                    self.log
                    'Trying to play file ' + wav_filename
                    wf = wave.open(wav_filename, 'rb')
                except IOError as ioe:
                    sys.stderr.write('IOError on file ' + wav_filename + '\n' + \
                                     str(ioe) + '. Skipping.\n')
                    return
                except EOFError as eofe:
                    sys.stderr.write('EOFError on file ' + wav_filename + '\n' + \
                                     str(eofe) + '. Skipping.\n')
                    return

                # Instantiate PyAudio.
                p = pyaudio.PyAudio()

                # Open stream.
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                output=True, start=True)

                data = wf.readframes(chunk_size)
                while len(data) > 0:
                    stream.write(data)
                    data = wf.readframes(chunk_size)

                # Stop stream.
                stream.stop_stream()
                stream.close()

                # Close PyAudio.
                p.terminate()
            except Exception as e:
                self.log("unable to play "+wav_filename)
                self.log(e)

    def press(self, pin):
        self.log("pressed: "+str(pin))

        self.last_press_time = time.time()

        if self.sequence_timeout > 0:
            if time.time() < self.sequence_timeout:
                self.log("timeout lock")
                return True

        # disable press lock, it may not get released with multiple pushes
        """ 
        if self.press_lock:
            # LOCK INPUT TO AVOID ISSUES WITH INPUT LAG
            self.log("input lock")
            return True
        """

        self.press_lock = True

        if self.filter_input(pin):
            self.log("ignoring this input")
            self.press_lock = False
            return True

        # IGNORE LAST PRESS BECAUSE INPUT ARE TRIGGERED MULTIPLE TIMES ON PRESS
        if pin != self.last_press:

            # CHECK IF INPUT IS EASTER EGG
            if pin == config.INPUT_EXTRA:
                self.run_action(pin)
                self.press_lock = False
                return True

            # SET TO LAST PIN
            self.last_press = pin

            # SEQ FOR MODE 1
            if self.mode == 2:
                # FREEPLAY, RUN EVERYTHING
                self.run_action(pin)
            else:

                # CHECK IF BUTTON IS NEXT IN SEQ
                self.log("seq check, pushed "+str(pin)+" expecting "+str(self.sequence[self.mode][self.mode_step]))
                self.log("mode step: "+str(self.mode_step))
                if pin == self.sequence[self.mode][self.mode_step]:
                    self.run_action(pin)
                    self.mode_step += 1

                    # CHECK IF THAT WAS THE LAST STEP
                    if self.mode_step == len(self.sequence[self.mode]):
                        self.sequence_timeout = int(time.time())+15
                        self.play(config.SOUNDS_COMPLETE)
                        self.flash_leds(20)
                        self.log("seq complete")
                        self.mode_step = 0
                        self.output_reset()
                        self.mode_set(self.mode)
                else:
                    # WRONG PRESS, START OVER
                    self.run_error()
                    self.mode_step = 0
                    self.output_reset()
                    self.mode_set(self.mode)
        self.press_lock = False
        self.log("press complete")

    def filter_input(self, pin):
        # FILTER INPUT PINS SO ONLY BUTTONS FOR SEQ ARE RAN
        for filter_pin in config.PIN_GROUP_INPUT_FILTER:
            if filter_pin == pin:
                # RETURN FALSE IF PIN IS ALLOWED
                return False
        # RETURN TRUE IF PIN SHOULD NOT BE USED
        return True

    def mode_toggle(self):
        # TURN OFF ANYTHING RUNNING
        self.output_reset()

        # SET MODE
        if (self.mode+1) > (len(config.PIN_GROUP_MODE)-1):
            self.mode = 0
        else:
            self.mode += 1
        self.mode_step = 0
        self.last_press = 0

        self.log("mode is now: "+str(self.mode))

        # RESET LEDS TO OFF
        for pin in config.PIN_GROUP_MODE:
            GPIO.output(pin, GPIO.HIGH)

        # TOGGLE ON LED
        GPIO.output(config.PIN_GROUP_MODE[self.mode], GPIO.LOW)

    def mode_set(self, mode):
        self.mode = mode
        self.mode_step = 0
        self.last_press = 0
        self.output_reset()

        # RESET LEDS TO OFF
        for pin in config.PIN_GROUP_MODE:
            GPIO.output(pin, GPIO.HIGH)

        # TOGGLE ON LED
        GPIO.output(config.PIN_GROUP_MODE[self.mode], GPIO.LOW)

    def output_reset(self):
        # TURN OFF ALL OUTPUTS
        self.log("turning off all outputs")
        for pin in config.PIN_GROUP_OUTPUT:
            GPIO.output(pin, GPIO.HIGH)

    def run_train(self):
        GPIO.output(config.PWR_TRAIN, GPIO.LOW)
        GPIO.output(config.LED_TRAIN, GPIO.LOW)

    def run_crosswalk(self):
        self.play(config.SOUNDS_CROSSWALK)
        GPIO.output(config.LED_CROSSWALK, GPIO.LOW)

    def run_crossing(self):
        GPIO.output(config.PWR_CROSSING, GPIO.LOW)
        GPIO.output(config.LED_CROSSING, GPIO.LOW)

    def run_signal(self):
        GPIO.output(config.LED_SIGNAL, GPIO.LOW)
        GPIO.output(config.LED_SIGNAL_RED, GPIO.LOW)
        time.sleep(1)
        GPIO.output(config.LED_SIGNAL_YELLOW, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(config.LED_SIGNAL_GREEN, GPIO.LOW)

    def run_eme(self):
        self.play(config.SOUNDS_SIREN)
        GPIO.output(config.LED_EME, GPIO.LOW)

    def run_error(self):
        self.play(config.SOUNDS_CRASH)

    def run_extra(self):
        self.play(config.SOUNDS_EXTRA)

    def run_action(self, pin):
        if pin == config.INPUT_TRAIN:
            self.run_train()
            return True

        if pin == config.INPUT_CROSSING:
            self.run_crossing()
            return True

        if pin == config.INPUT_SIGNAL:
            self.run_signal()
            return True

        if pin == config.INPUT_CROSSWALK:
            self.run_crosswalk()
            return True

        if pin == config.INPUT_EME:
            self.run_eme()
            return True

        if pin == config.INPUT_EXTRA:
            self.run_extra()
            return True

        self.log("warning, pin has no run handler: "+str(pin))

    def flash_leds(self, cycles):
        cycle = 0
        while cycle != cycles:
            self.log("flashing leds")
            for pin in config.PIN_GROUP_OUTPUT_LEDS:
                GPIO.output(pin, GPIO.LOW)
            time.sleep(.2)
            for pin in config.PIN_GROUP_OUTPUT_LEDS:
                GPIO.output(pin, GPIO.HIGH)
            time.sleep(.2)
            cycle += 1

    def log(self, text):

        print(text)
        if config.LOG_ENABLED:
            now = datetime.datetime.now()
            if not os.path.isdir(config.CRASH_PATH):
                os.mkdir(config.CRASH_PATH)

            with open(config.CRASH_PATH + 'log_'+str(now.year)+str(now.month)+str(now.day)+'_'+'.txt', 'a') as out:
                out.write(str(str(now.month)+'/'+str(now.day)+'/'+str(now.year)+' '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+' - '+text )+'\n')


