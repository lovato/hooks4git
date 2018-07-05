# -*- coding: utf-8 -*-
template = '''#!/usr/bin/env python

import os
import sys
import subprocess
import configparser

# available settings list
AVAILABLE_SETTINGS = (
    'exclude', 'filename', 'select', 'ignore', 'max-line-length', 'count', 'config',
    'quiet', 'show-pep8', 'show-source', 'statistics', 'verbose', 'max-complexity'
)

SETTINGS_WITH_PARAMS = (
    'exclude', 'filename', 'select', 'ignore', 'max-line-length', 'format'
)

# colorize output
COLOR = {
    'red': '\\033[1;31m',
    'green': '\\033[1;32m',
    'yellow': '\\033[1;33m',
}


def parse_settings(config_file):
    """
    Get pep8 and flake8 lint settings from config file.
    Useful for define per-project lint options.
    """
    settings = {'pep8': list(), 'flake8': list()}
    # read project settings
    if not os.path.exists(config_file) or not os.path.isfile(config_file):
        return settings
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
    except configparser.MissingSectionHeaderError as e:
        print("ERROR: project lint config file is broken:\\n")
        print(repr(e))
        sys.exit(1)
    # read project lint settings for pep8 and flake8
    for linter in settings.keys():
        try:
            for key, value in config.items(linter):
                if key in AVAILABLE_SETTINGS:
                    if key in SETTINGS_WITH_PARAMS:
                        settings[linter].append("--{}={}".format(key, value))
                    else:
                        settings[linter].append("--{}".format(key))
                else:
                    print("WARNING: unknown {} linter config: {}".format(linter, key))
        except configparser.NoSectionError:
            pass
    return settings


def system(*args, **kwargs):
    """
    Run system command.
    """
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, err = proc.communicate()
    return out


def get_changed_files():
    """
    Get python files from 'files to commit' git cache list.
    """
    files = []
    filelist = system('git', 'diff', '--cached', '--name-status').strip()
    for line in str(filelist.decode('utf-8')).split('\\n'):
        try:
            action, filename = line.strip().split()
            if filename.endswith('.py') and action != 'D':
                files.append(filename)
        except Exception as ex:
            pass
    return files


def lint(cmd, files, settings):
    """
    Run pep8 or flake8 lint.
    """
    if cmd not in ('pep8', 'flake8'):
        raise Exception("Unknown lint command: {}".format(cmd))
    args = settings[:]
    args.insert(0, cmd)
    args.extend(files)
    return str(system(*args).decode('utf-8')).strip().split('\\n')


def main():
    """
    Do work
    """
    files = get_changed_files()
    if not files:
        print("Python lint: {}SKIP \033[m".format(COLOR['yellow']))
        return
    config_file = os.path.join(os.path.abspath(os.curdir), '.flake8')
    settings = parse_settings(config_file)
    errors = lint('flake8', files, settings['flake8'])

    if not len(errors) or errors[0] is '':
        print("Python lint: {}OK \033[m".format(COLOR['green']))
        return
    print("Python lint: {}FAIL".format(COLOR['red']))
    print("\\n".join(sorted(errors)))
    print("\033[m")
    print("Aborting commit due to python lint errors.")
    sys.exit(1)


if __name__ == '__main__':
    main()


'''
