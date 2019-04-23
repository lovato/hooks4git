# -*- coding: utf-8 -*-

# from setuptools.command.install import install
import sys
import os
import shutil
from hooks4git.hook import system
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


def get_hooks_path(git_root_path):
    if git_root_path is None:
        print("I am afraid I can't to that. You are not inside a GIT repo. Reach one and re-run this tool.")
        return None
    if git_root_path.endswith("/.git") is False:
        print("Humm, this is odd. Your GIT repo must have a .git folder. Looks like you are not inside a GIT repo.")  # noqa
        return None
    hooks_path = os.path.join(git_root_path, "hooks")
    if not os.path.isdir(hooks_path):
        message = "Looks like your '.git/hooks' folder is missing."
        print("%s Let's try to fix this..." % message)
        try:
            os.makedirs(hooks_path)
            print("Cool! '.git/hooks' folder was created.")
            return hooks_path
        except:  # noqa
            return None
    else:
        return hooks_path


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

        path = os.path.abspath(path)
        setup_path = os.path.abspath(setup_path)
        hooks_path = get_hooks_path(git_path)
        if hooks_path:
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
            print("Wow! hooks4git files were installed successfully! Thanks for hooking!")
            print("If you are a courious person, take a look at .git/hooks folder.")
            print("TIP: To get rid of hooks, comment lines on the .hooks4git.ini file.")
        return True
