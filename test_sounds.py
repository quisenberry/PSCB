import config
from  pscb import PSCB

app = PSCB()
for sound in config.SOUNDS:
    print(sound)
    app.play_wav(sound)