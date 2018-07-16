'''
This is used to manage remote deployments


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

import config
import time
import git
import os
import traceback
from pscb import PSCB

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
        out.write('------------------------')
        out.write(traceback.format_exc())


if __name__ == '__main__':
    # LOOP FOR CHECKING IF GIT REPO HAS CHANGED
    print(str(time.ctime()) + ": Checking for updates")

    repo = git.Repo(config.PATH_ABSOLUT)
    current_hash = repo.head.object.hexsha
    print(current_hash)

    try:
        o = repo.remotes.origin
        o.pull()
        pull_hash = repo.head.object.hexsha
    except Exception as e:
        print("warning: unable to check repo, is internet connected?")
        # print(e)
        time.sleep(10)
        pull_hash = current_hash
    if current_hash != pull_hash:
        print("changed")
    else:
        print("repo is current")

    try:
        app = PSCB('deploy.py')

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
        print(traceback.format_exc())
        print("closing")

    finally:
        try:
            GPIO.cleanup()
        except:
            print("GPIO Clean Up failed")
            # ignore, if we can clean up there is nothing we can do





