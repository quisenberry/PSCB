'''
This config holds all user adjustable vars. Vars should not be changed directly on the Pi but in the GIT repo then
pushed and auto updated. Changing vars here will break the auto update system.


Author: Ryan Mills <ryan@flexhibit.com>
Copyright (c) 2018 Flexhibit - All Rights Reserved

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import os
import sys

# DEPLOY VARS
GIT_POLL_RATE = 5 #time in seconds the script should check for GIT updates
GIT_REPO = 'https://github.com/quisenberry/PSCB.git'
GIT_REPO_LOCAL = os.path.dirname(os.path.abspath(sys.argv[0]))
DEPLOY_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))+os.path.sep+'exhibit.py'


# MAIN
PSCB_NAME = 'PSCB'
PSCB_VERISON = '0.0.2'

# SOUNDS
SOUNDS_PATH = 'sounds'+os.sep
SOUNDS_SIREN = SOUNDS_PATH+'siren.wav'
SOUNDS_HORN = SOUNDS_PATH+'horn.wav'


# PIN MAPPING
INPUT_TRAIN = 2
INPUT_CROSSING = 3
INPUT_SIGNAL = 4
INPUT_EME = 5
INPUT_CROSSWALK = 6
INPUT_EXTRA = 7
INPUT_MODE = 24

PWR_TRAIN = 8
PWR_CROSSING = 9

LED_MODE1 = 10
LED_MODE2 = 11
LED_MODE3 = 12
LED_TRAIN = 13
LED_SIGNAL_GREEN = 14
LED_SIGNAL_YELLOW = 15
LED_SIGNAL_RED = 16
LED_CROSSWALK = 17
LED_EME = 18

PIN_GROUP_INPUT = [INPUT_TRAIN, INPUT_CROSSING, INPUT_SIGNAL, INPUT_EME, INPUT_CROSSWALK, INPUT_EXTRA, INPUT_MODE]
PIN_GROUP_OUTPUT = [
    PWR_TRAIN,
    PWR_CROSSING,
    LED_MODE1,
    LED_MODE2,
    LED_MODE3,
    LED_TRAIN,
    LED_SIGNAL_GREEN,
    LED_SIGNAL_YELLOW,
    LED_SIGNAL_RED,
    LED_CROSSWALK,
    LED_EME]
PIN_GROUP_MODE = [LED_MODE1, LED_MODE2, LED_MODE3]



