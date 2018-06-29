import config
import wave
import pyaudio
import pyttsx3
import time

try:
    import RPi.GPIO as GPIO
    DEVICE_MODE = 'pi'
except Exception as e:
    DEVICE_MODE = 'test'
    from EmulatorGUI import GPIO



class PSCB:
    sound = False
    mode = 0

    def Main(self):
        #INIT TEXT TO SPEECH

        self.sound = pyttsx3.init()
        self.sound.setProperty('voice', 'english+f3')
        rate = self.sound.getProperty('rate')
        self.sound.setProperty('rate', rate - 40)
        self.sound.say('Running Exhibit LED check')
        self.sound.runAndWait()

        #INIT GPIO

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        #INIT PINS
        for pin in config.PIN_GROUP_INPUT:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        for pin in config.PIN_GROUP_OUTPUT:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

        for pin in config.PIN_GROUP_OUTPUT:
            print(str(pin))
            GPIO.output(pin, GPIO.LOW)
            time.sleep(1)

        while True:
            time.sleep(1)

        #self.play_wav(config.SOUNDS_HORN)


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

app = PSCB()
app.Main()