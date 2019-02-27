import os
import subprocess
import copy


def git_get_config(key):
    return subprocess.check_output(['git', 'config', '--get', key]).decode().strip()


def git_set_config(key, value):
    subprocess.check_call(['git', 'config',  key, value])


homework_dirs = list(map(os.path.abspath, filter(os.path.isdir, os.scandir())))
for i in homework_dirs:
    print('Scanning', i)
    git_path = os.path.join(i, ".git")
    if os.path.isdir(git_path):
        print('Found git', git_path)
        os.chdir(git_path)
        print(git_get_config('core.autocrlf'))
        print(git_get_config('core.safecrlf'))
        print(git_get_config('user.name'))
        print(git_get_config('user.email'))
        os.chdir(i)
