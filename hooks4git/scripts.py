# -*- coding: utf-8 -*-

from setuptools.command.install import install
import os
import shutil
import subprocess

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

    # TODO: Fix this for Python 2.7
    # try:
    #     input = raw_input
    # except NameError:
    #     pass

    while True:
        print('>>>> ' + question + prompt)
        choice = input().lower()
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
            print(dest)
            if query_yes_no('Target file exists. Can I replace it?'):
                shutil.copy(src, dest)
            else:
                print('Your file was left untouched. Please consider upgrading it.')
        else:
            shutil.copy(src, dest)
    else:
        if not os.path.isfile(dest):
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
        # setup_path = os.path.join(system('git', 'rev-parse', '--show-toplevel')[1].replace('\n', ''), 'hooks4git')
        setup_path = os.path.dirname(os.path.realpath(__file__))
        if 'site-packages' in setup_path:
            global standalone_run
            standalone_run = True
        path = os.path.abspath(path)
        setup_path = os.path.abspath(setup_path)
        if not os.path.isdir(os.path.join(git_path, "hooks")):
            message = '*****************************************************************\n'
            message += '* hooks4git is installed. Just run "hooks4git" to install the hooks.'
            print(message)
        else:
            origin_yml = os.path.join(setup_path, '.hooks4git.yml')
            target_yml = os.path.join(path, '.hooks4git.yml')
            if os.path.isfile(target_yml):
                target_yml = target_yml + '.NEWVERSION'
            copy(origin_yml, target_yml)
            files_to_copy = system('ls', os.path.join(setup_path, 'git/hooks'))
            for file in files_to_copy[1].split('\n'):
                if file not in ['__pycache__', '', 'hooks4git.py']:
                    src = os.path.join(setup_path, 'git/hooks', file)
                    target = os.path.join(git_path, 'hooks', file)
                    copy(src, target)
            print("Precommit scripts added successfully, continuing ...")
            print("TIP: If you want to get rid of the hooks, just delete the .hooks4git.yml from your project folder.")
        return True


class Post_install(install):
    def run(self):
        install.run(self)
        Exec.add_hooks()
