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
import errno
import os
import sys


PID = 0

def pid_exists(pid):
    """Check whether pid exists in the current process table.
    UNIX only.
    """
    if pid < 0:
        return False
    if pid == 0:
        # According to "man 2 kill" PID 0 refers to every process
        # in the process group of the calling process.
        # On certain systems 0 is a valid PID but we have no way
        # to know that in a portable fashion.
        raise ValueError('invalid PID 0')
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            # ESRCH == No such process
            return False
        elif err.errno == errno.EPERM:
            # EPERM clearly means there's a process to deny access to
            return True
        else:
            # According to "man 2 kill" possible error values are
            # (EINVAL, EPERM, ESRCH)
            raise
    else:
        return True



def main():
    #START PRIMARY SCRIPT

    #LOOP FOR CHECKING IF GIT REPO HAS CHANGED
    print(str(time.ctime())+": Checking for updates")

    repo = git.Repo(config.PATH_ABSOLUT)
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
        process = subprocess.Popen([sys.executable, config.DEPLOY_PATH])
    else:
        print("repo is current")

    process = subprocess.Popen([sys.executable, config.DEPLOY_PATH])
    PID = process.pid

    while True:
        if pid_exists(PID):
            print("script is running")
        else:
            print("script has crashed, restarting")
            process = subprocess.Popen([sys.executable, config.DEPLOY_PATH])
            PID = process.pid
        time.sleep(20)




if __name__ == '__main__':
    main()