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

# DEPLOY VARS
GIT_POLL_RATE = 5 #time in seconds the script should check for GIT updates
GIT_REPO = 'https://github.com/quisenberry/PSCB.git'
DEPLOY_PATH = os.getcwd()+os.sep+'pscb.py'


# MAIN
PSCB_NAME = 'PSCB'
PSCB_VERISON = '0.0.6'

# SOUNDS
SOUNDS_PATH = 'sounds'+os.sep
SOUNDS_SIREN = SOUNDS_PATH+'siren.wav'
SOUNDS_HORN = SOUNDS_PATH+'horn.wav'
