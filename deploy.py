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
import sys
import subprocess
import pyttsx3



def main():
    #START PRIMARY SCRIPT
    process = subprocess.Popen([sys.executable, config.DEPLOY_PATH])
    print(process.pid)

    #INIT TEXT TO SPEECH
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'english+f3')
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 30)

    #LOOP FOR CHECKING IF GIT REPO HAS CHANGED
    while True:
        print(str(time.ctime())+": Checking for updates")

        repo = git.Repo(config.GIT_REPO_LOCAL)
        current_hash = repo.head.object.hexsha
        print(current_hash)

        try:
            o = repo.remotes.origin
            o.pull()
            pull_hash = repo.head.object.hexsha
        except Exception as e:
            print("warning: unable to check repo, is internet connected?")
            #print(e)
            time.sleep(10)
            pull_hash = current_hash
        if current_hash != pull_hash:
            print("changed")
            engine.say('Please wait. I\'m updating the exhibit.')
            engine.runAndWait()
            process.kill()
            process = subprocess.Popen([sys.executable, config.DEPLOY_PATH])
        else:
            print("repo is current")
        time.sleep(config.GIT_POLL_RATE)



if __name__ == '__main__':
    main()