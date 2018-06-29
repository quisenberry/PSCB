import config
import wave
import pyaudio
import pyttsx3
import time
import sys

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

    def main(self):
        #INIT TEXT TO SPEECH
        self.init_speech()
        self.say("Starting Exhibit")
        self.say('mode '+DEVICE_MODE)
        #INIT GPIO
        GPIO.setmode(GPIO.BCM)
        #GPIO.setwarnings(False)


        #INIT PINS
        self.init_pins()

        #INIT INPUT (not supported in EmulatorGUI)
        if DEVICE_MODE == 'pi':
            self.init_input()

        #TEST AUDIO
        self.test_audio()
        time.sleep(1)

        #TEST OUTPUT PINS
        self.test_output()
        time.sleep(1)


    def init_speech(self):
        self.sound = pyttsx3.init()
        self.sound.setProperty('voice', 'english+f3')
        rate = self.sound.getProperty('rate')
        self.sound.setProperty('rate', rate - 40)

    def init_pins(self):
        self.say('setting input output pins')
        for pin in config.PIN_GROUP_INPUT:
            print("setting pin "+str(pin)+" as input")
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
        for pin in config.PIN_GROUP_OUTPUT:
            print("setting pin "+str(pin)+" as output")
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
            GPIO.output(pin, GPIO.LOW)
            print("state: "+GPIO.output(pin))

    def init_input(self):
        for pin in config.PIN_GROUP_INPUT:
            GPIO.add_event_detect(pin, GPIO.FALLING, self.press)

    def test_audio(self):
        self.say('Testing audio playback')
        time.sleep(1)
        self.play_wav(config.SOUNDS_HORN)

    def test_output(self):
        self.say("Toggling each relay on and off")

        #CYCLE ON EACH RELAY ONE AT A TIME
        for pin in config.PIN_GROUP_OUTPUT:
            print("testing output pin: "+str(pin))
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(pin, GPIO.LOW)

        time.sleep(1)
        self.say("relay test complete")

    def test_input(self):
        self.say("press mode test enabled")
        while True:
            while GPIO.input(config.INPUT_MODE) == GPIO.HIGH:
                time.sleep(0.01)
            print("mode button pressed")
            self.set_mode()
            while GPIO.input(config.INPUT_MODE) == GPIO.LOW:
                time.sleep(0.01)

    def play_wav(self, wav_filename, chunk_size=1024):
        '''
        Play (on the attached system sound device) the WAV file
        named wav_filename.
        '''

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
                        output=True)

        data = wf.readframes(chunk_size)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(chunk_size)

        # Stop stream.
        stream.stop_stream()
        stream.close()

        # Close PyAudio.
        p.terminate()

    def say(self, text):
        self.sound.say(text)
        self.sound.runAndWait()

    def press(self, pin):
        print("pressed: "+str(pin))

    def set_mode(self):
        #interat thru modes
        if (self.mode+1) > (len(config.PIN_GROUP_MODE)-1):
            self.mode = 0
        else:
            self.mode += 1
        print("mode is now: "+str(self.mode))

        # RESET LEDS TO OFF
        for pin in config.PIN_GROUP_MODE:
            GPIO.output(pin, GPIO.LOW)
        GPIO.output(config.PIN_GROUP_MODE[self.mode], GPIO.HIGH)

