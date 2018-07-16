import time
import git
import config


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
        print("repo updated")
    else:
        print("repo is current")