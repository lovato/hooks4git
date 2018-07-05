# -*- coding: utf-8 -*-

from setuptools.command.install import install
from hooks4git.extras import template
import stat
import os
import sys


class Exec:
    @staticmethod
    def add_pre_commit(path=os.environ["PWD"]):
        # if .git/hooks directory does not exist (which means a non valid git repo)
        if not os.path.isdir(os.path.join(path, ".git/hooks")):
            message = '*****************************************************************\n'
            message += '* Oops, this hook can only be installed on a local GIT repository\n'
            message += '* Please, make sure to do a "git init" on this folder.'
            print(message)
            sys.exit(1)

        # Ok, it is a GIT repository...
        with open('{}/.git/hooks/pre-commit'.format(path), 'wb') as f:
            f.write(template.encode())
            # Adding executable flag to the file
            st = os.stat('{}/.git/hooks/pre-commit'.format(path))
            os.chmod('{}/.git/hooks/pre-commit'.format(path), st.st_mode | stat.S_IEXEC)
        print("Precommit script added successfully, continuing ...")
        return True


class Post_install(install):
    def run(self):
        install.run(self)
        Exec.add_pre_commit()
