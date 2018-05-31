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
import subprocess


def main():
    process = subprocess.Popen(config.DEPLOY_PATH + " 1", shell=True, stdout=subprocess.PIPE)
    while True:
        print(str(time.ctime())+": Checking for updates")
        repo = git.Repo()
        current_hash = repo.head.object.hexsha
        o = repo.remotes.origin
        o.pull()
        pull_hash = repo.head.object.hexsha
        if current_hash != pull_hash:
            print("changed")
            process.kill()
            process = subprocess.Popen(config.DEPLOY_PATH + " 1", shell=True, stdout=subprocess.PIPE)
        time.sleep(config.GIT_POLL_RATE)



if __name__ == '__main__':
    main()