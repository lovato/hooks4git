# -*- coding: utf-8 -*-

from setuptools.command.install import install
# import stat
import os
# import sys


class Exec:
    @staticmethod
    def add_hooks(path=os.environ["PWD"]):
        # if .git/hooks directory does not exist (which means a non valid git repo)
        if not os.path.isdir(os.path.join(path, ".git/hooks")):
            message = '*****************************************************************\n'
            message += '* Oops, hooks can only be installed on a GIT repository\n'
            message += '* Please, make sure to do a "git init" on this folder.\n\n'
            message += '* hooks4git is installed anyway. Then, just run "hooks4git" to install the hooks.'
            print(message)
        else:
            # TODO: Tell the user we are just about to change his filesystem. Ask for permission.
            # Ok, it is a GIT repository...
            # with open('{}/.git/hooks/pre-commit'.format(path), 'wb') as f:
            #     f.write(pre_commit.encode())
            #     # Adding executable flag to the file
            #     st = os.stat('{}/.git/hooks/pre-commit'.format(path))
            #     os.chmod('{}/.git/hooks/pre-commit'.format(path), st.st_mode | stat.S_IEXEC)
            # TODO: just copy the files!!! and the yml
            print("Precommit script added successfully, continuing ...")
        return True


class Post_install(install):
    def run(self):
        install.run(self)
        Exec.add_hooks()
