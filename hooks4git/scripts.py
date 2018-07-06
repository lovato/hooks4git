# -*- coding: utf-8 -*-

from setuptools.command.install import install
# import stat
import os
# import sys
import shutil
# import errno
import subprocess


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        print('>>>> ' + question + prompt)
        # TODO: Python 2.7 é "input_raw"
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def copy(src, dest):
    print('From: %s' % src)
    print('To: %s' % dest)
    if os.path.isfile(dest):
        if query_yes_no('Target file exists. Can I replace it?'):
            pass
            # shutil.copy(src, dest)
        else:
            print('Your file was left untouched.')
    else:
        shutil.copy(src, dest)


def system(*args, **kwargs):
    """
    Run system command.
    """
    try:
        kwargs.setdefault('stdout', subprocess.PIPE)
        proc = subprocess.Popen(args, **kwargs)
        out = proc.communicate()[0]
        out = out.decode('utf-8')
        out = str(out)
        returncode = proc.returncode
    except Exception as e:  # noqa
        out = str(e)
        returncode = -1
    return returncode, out


class Exec:
    @staticmethod
    def add_hooks(path=os.environ["PWD"]):
        print('Current Working Folder: %s' % path)
        path = system('git', '-C', path, 'rev-parse', '--show-toplevel')[1].replace('\n', '')
        git_path = system('git', '-C', path, 'rev-parse', '--git-dir')[1].replace('\n', '')
        if git_path == '.git':
            git_path = os.path.join(path, git_path)
        setup_path = system('git', 'rev-parse', '--show-toplevel')[1].replace('\n', '')
        # if .git/hooks directory does not exist (which means a non valid git repo)
        path = os.path.abspath(path)
        setup_path = os.path.abspath(setup_path)
        if not os.path.isdir(os.path.join(git_path, "hooks")):
            message = '*****************************************************************\n'
            message += '* Oops, hooks can only be installed on a GIT repository\n'
            message += '* Please, make sure to do a "git init" on this folder.\n\n'
            message += '* hooks4git is installed anyway. Then, just run "hooks4git" to install the hooks.'
            print(message)
        else:
            files_to_copy = system('ls', os.path.join(setup_path, 'hooks4git/git/hooks'))
            for file in files_to_copy[1].split('\n'):
                if file not in ['__pycache__', '', 'hooks4git.py']:
                    src = os.path.join(setup_path, 'hooks4git/git/hooks', file)
                    target = os.path.join(git_path, 'hooks', file)
                    copy(src, target)
            # copy(os.path.join(setup_path, 'hooks4git/git/hooks'), '{}/hooks'.format(git_path))
            copy(os.path.join(setup_path, 'hooks4git/.hooks4git.yml'), os.path.join(path, '.hooks4git.yml'))
            print("Precommit scripts added successfully, continuing ...")
            print("TIP: If you want to get rid of the hooks, just delete the .hooks4git.yml from your project.")
        return True


class Post_install(install):
    def run(self):
        install.run(self)
        Exec.add_hooks()
