import config
from  pscb import PSCB

app = PSCB('test_sounds.py')
for sound in config.SOUNDS:
    print(sound)
    app.play_wav(sound)