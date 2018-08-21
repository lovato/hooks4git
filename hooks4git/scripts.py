# -*- coding: utf-8 -*-

from setuptools.command.install import install
import sys
import os
import shutil
import subprocess
from hooks4git import __version__
import ast

standalone_run = False


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

    if sys.version_info[:2] <= (2, 7):
        # If this is Python 2, use raw_input()
        get_input = ast.literal_eval('raw_input')
    else:
        get_input = ast.literal_eval('input')

    while True:
        print('>>>> ' + question + prompt)
        choice = get_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def copy(src, dest):
    # print('From: %s' % src)
    # print('To: %s' % dest)
    if standalone_run:
        if os.path.isfile(dest):
            # print(dest)
            # if query_yes_no('Target file exists. Can I replace it?'):
            shutil.copy(src, dest)
            # else:
            #     print('Your file was left untouched. Please consider upgrading it.')
        else:
            shutil.copy(src, dest)
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
        # print('Current Working Folder: %s' % path)
        # setup_path = os.path.join(system('git', 'rev-parse', '--show-toplevel')[1].replace('\n', ''), 'hooks4git')
        setup_path = os.path.dirname(os.path.realpath(__file__))
        if 'site-packages' in setup_path:
            global standalone_run
            standalone_run = True
        try:
            path = system('git', '-C', path, 'rev-parse', '--show-toplevel')[1].replace('\n', '')
            git_path = system('git', '-C', path, 'rev-parse', '--git-dir')[1].replace('\n', '')
            if git_path == '.git':
                git_path = os.path.join(path, git_path)
        except:  # noqa
            git_path = None

        if git_path:
            path = os.path.abspath(path)
            setup_path = os.path.abspath(setup_path)
            if os.path.isdir(os.path.join(git_path, "hooks")):
                origin_config = os.path.join(setup_path, '.hooks4git.ini')
                target_config = os.path.join(path, '.hooks4git.ini')
                if os.path.isfile(target_config):
                    target_config = target_config.replace('.ini', '-' + __version__ + '.ini')
                copy(origin_config, target_config)
                files_to_copy = system('ls', os.path.join(setup_path, 'git/hooks'))
                for file in files_to_copy[1].split('\n'):
                    if file not in ['__pycache__', '', 'hooks4git.py']:
                        src = os.path.join(setup_path, 'git/hooks', file)
                        target = os.path.join(git_path, 'hooks', file)
                        copy(src, target)
                print("\nhooks4git scripts and files copied successfully! Thanks for hooking!")
                print("TIP: If you want to get rid of the hooks, just delete the .hooks4git.ini from your project.")
            else:
                if not standalone_run:
                    message = '*****************************************************************\n'
                    message += '* hooks4git is installed. Just run "hooks4git" to install the hooks.'
                    print(message)
                else:
                    print("I am afraid I can't to that. Looks like your .git folder is not standard.")
        else:
            print("I am afraid I can't to that. You are not inside a GIT repo. Reach one and re-run this tool.")
        return True


class Post_install(install):
    def run(self):
        install.run(self)
        Exec.add_hooks()
