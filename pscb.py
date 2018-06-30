import config
import wave
import pyaudio
import pyttsx3
import time
import sys
import threading

try:
    import RPi.GPIO as GPIO
    DEVICE_MODE = 'pi'
except Exception as e:
    DEVICE_MODE = 'test'
    from EmulatorGUI import GPIO


class PSCB:
    sound = False
    mode = 0
    mode_press_state = False
    mode_sequence_current = 0
    mode_sequence_1 = [
        config.INPUT_TRAIN,
        config.INPUT_CROSSING,
        config.INPUT_SIGNAL,
        config.INPUT_CROSSWALK,
        config.INPUT_EME
    ]

    mode_sequence_2 = [
        config.INPUT_EME,
        config.INPUT_SIGNAL,
        config.INPUT_TRAIN,
        config.INPUT_CROSSING
    ]
    mode_step = 0
    last_press = 0

    def __init__(self):
        # INIT TEXT TO SPEECH
        self.init_speech()

        # INIT GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # INIT PINS
        self.init_pins()


    def start_exhibit(self):
        self.mode_set(0)

        # INIT INPUT (not supported in EmulatorGUI)
        if DEVICE_MODE == 'pi':
            self.init_input()

        # TEST AUDIO
        #self.test_audio()

        # INIT MODE BUTTON (Mode is polled) nothing can be called after this
        self.monitor_mode_btn()

    def init_speech(self):
        self.sound = pyttsx3.init()
        self.sound.setProperty('voice', 'english+f3')
        rate = self.sound.getProperty('rate')
        self.sound.setProperty('rate', rate - 40)

    def init_pins(self):
        for pin in config.PIN_GROUP_INPUT:
            print("setting pin "+str(pin)+" as input")
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        for pin in config.PIN_GROUP_OUTPUT:
            print("setting pin "+str(pin)+" as output")
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)

    def init_input(self):
        for pin in config.PIN_GROUP_INPUT:
            GPIO.add_event_detect(pin, GPIO.FALLING, self.press)

    def test_audio(self):
        self.say('Testing audio playback')
        time.sleep(1)
        self.play_wav(config.SOUNDS_CRASH)

    def test_output_pins(self):
        # CYCLE ON EACH RELAY ONE AT A TIME
        for pin in config.PIN_GROUP_OUTPUT:
            print("testing output pin: "+str(pin))
            GPIO.output(pin, GPIO.LOW)
            time.sleep(1)
            GPIO.output(pin, GPIO.HIGH)

        time.sleep(1)
        self.say("relay test complete")

    def monitor_mode_btn(self):
        while True:
            while GPIO.input(config.INPUT_MODE) == GPIO.HIGH:
                time.sleep(0.01)
            print("mode button pressed")
            self.mode_toggle()
            while GPIO.input(config.INPUT_MODE) == GPIO.LOW:
                time.sleep(0.01)

    def play(self, wave_file):
        t = threading.Thread(target=self.play_wav, args=(wave_file,))
        t.daemon = True
        t.start()

    def play_wav(self, wav_filename, chunk_size=1024):
        '''
        Play (on the attached system sound device) the WAV file
        named wav_filename.
        '''
        try:
            try:
                print
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
            print("unable to play "+wav_filename)
            print(e)

    def say(self, text):
        self.sound.say(text)
        self.sound.runAndWait()

    def press(self, pin):
        print("pressed: "+str(pin))

        if self.filter_INPUT(pin):
            print("ignoring this input")
            return True

        # IGNORE LAST PRESS BECAUSE INPUT ARE TRIGGERED MULTIPLE TIMES ON PRESS
        if pin != self.last_press:

            # CHECK IF INPUT IS EASTER EGG
            if pin == config.INPUT_EXTRA:
                self.run_action(pin)
                return True

            # SET TO LAST PIN
            self.last_press = pin

            # SEQ FOR MODE 1
            if self.mode == 0:

                # CHECK IF BUTTON IS NEXT IN SEQ
                print("seq check, pushed "+str(pin)+" expecting "+str(self.mode_sequence_1[self.mode_step]))
                if pin == self.mode_sequence_1[self.mode_step]:
                    self.run_action(pin)
                    self.mode_step += 1

                    # CHECK IF THAT WAS THE LAST STEP
                    if self.mode_step == len(self.mode_sequence_1):
                        print("seq complete")
                        time.sleep(10)
                        self.mode_step = 0
                        self.output_reset()
                        self.mode_set(self.mode)
                else:
                    # WRONG PRESS, START OVER
                    self.run_error()
                    self.mode_step = 0
                    self.output_reset()
                    self.mode_set(self.mode)

            elif mode == 1:

                # CHECK IF BUTTON IS NEXT IN SEQ
                print("seq check, pushed " + str(pin) + " expecting " + str(self.mode_sequence_2[self.mode_step]))
                if pin == self.mode_sequence_2[self.mode_step]:
                    self.run_action(pin)
                    self.mode_step += 1

                    # CHECK IF THAT WAS THE LAST STEP
                    if self.mode_step == len(self.mode_sequence_2):
                        print("seq complete")
                        time.sleep(10)
                        self.mode_step = 0
                        self.output_reset()
                        self.mode_set(self.mode)
                else:
                    # WRONG PRESS, START OVER
                    self.run_error()
                    self.mode_step = 0
                    self.output_reset()
                    self.mode_set(self.mode)
            else:
                # FREEPLAY, RUN EVERYTHING
                self.run_action(pin)

    def filter_input(self, pin):
        # FILTER INPUT PINS SO ONLY BUTTONS FOR SEQ ARE RAN
        for filter_pin in config.PIN_GROUP_INPUT_FILTER:
            if filter_pin == pin:
                # RETURN FALSE IF PIN IS ALLOWED
                return False
        # RETURN TRUE IF PIN SHOULD NOT BE USED
        return True

    def mode_toggle(self):
        # SET MODE
        if (self.mode+1) > (len(config.PIN_GROUP_MODE)-1):
            self.mode = 0
        else:
            self.mode += 1
        self.mode_step = 0

        print("mode is now: "+str(self.mode))

        # RESET LEDS TO OFF
        for pin in config.PIN_GROUP_MODE:
            GPIO.output(pin, GPIO.HIGH)

        # TOGGLE ON LED
        GPIO.output(config.PIN_GROUP_MODE[self.mode], GPIO.LOW)

    def mode_set(self, mode):
        self.mode = mode
        self.mode_step = 0
        self.output_reset()

        # RESET LEDS TO OFF
        for pin in config.PIN_GROUP_MODE:
            GPIO.output(pin, GPIO.HIGH)

        # TOGGLE ON LED
        GPIO.output(config.PIN_GROUP_MODE[self.mode], GPIO.LOW)

    def output_reset(self):
        for pin in config.PIN_GROUP_OUTPUT:
            print("setting pin "+str(pin)+" as output")
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

        print("warning, pin has no run handler: "+str(pin))

