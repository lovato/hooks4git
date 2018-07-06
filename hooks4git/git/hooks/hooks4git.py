#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import yaml
import sys
from colorama import Fore
from colorama import Style

error = False


def out(msg_type, msg, color=Fore.WHITE):
    label = color + '[ ' + msg_type + ' ]'
    if msg_type == 'FAIL':
        label = Fore.RED + '[  FAIL  ]'
    if msg_type == 'INFO':
        label = Fore.BLUE + '[  INFO  ]'
    if msg_type == 'WARN':
        label = Fore.YELLOW + '[  WARN  ]'
    if msg_type == 'PASS':
        label = Fore.GREEN + '[  PASS  ]'
    print('\n' + Style.BRIGHT + label + ' ' + Style.RESET_ALL + msg)


def system(*args, **kwargs):
    """
    Run system command.
    """
    try:
        kwargs.setdefault('stdout', subprocess.PIPE)
        proc = subprocess.Popen(args, **kwargs)
        out, err = proc.communicate()
        out = out.decode('utf-8')
        out = str(out).strip().replace('\n', '\n• ')
        returncode = proc.returncode
    except Exception as e:  # noqa
        out = str(e)
        returncode = -1
    if len(out) < 1:
        out = '• None'
    else:
        out = '• ' + out + Style.RESET_ALL

    return returncode, out


def execute(step, cmd, files, settings):
    """
    Prepare system command.
    """
    # if cmd not in ('pep8', 'flake8'):
    #     raise Exception("Unknown lint command: {}".format(cmd))
    args = settings[:]
    args.insert(0, cmd)
    args.extend(files)
    out("INFO", "Script %s\n%s$ %s%s\n\nOutput:" % (step, Style.BRIGHT, ' '.join(args), Style.RESET_ALL))

    return system(*args)


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
        except Exception as ex:  # noqa
            pass
    return files


def main():
    cmd = os.path.basename(__file__)
    with open("../../.hooks4git.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    step = 0
    try:
        cfg = cfg.get('hooks')
        commands = cfg.get(cmd, {'scripts': []}).get('scripts', [])
        if len(commands) > 0:
            title = "hooks4git :: %s Hook Called" % cmd.title()
            title = Fore.YELLOW + Style.BRIGHT + title + Style.RESET_ALL
            print(title)
        for command in commands:
            step += 1
            result = execute(step, command.split()[0], [], command.split()[1:])
            print(result[1])
            if result[0] != 0:
                global error
                error = True
                out('FAIL', "%s'%s' step failed to execute%s" % (Fore.RED, command.split()[0], Style.RESET_ALL))
            else:
                out('PASS', "%s'%s' step executed successfully%s" % (Fore.GREEN, command.split()[0], Style.RESET_ALL))

    except Exception as e:  # noqa
        # print(e)
        pass
    # if step == 0:
    #     print("%s There was no step configured for %s." % (colored('[Ignore]', 'green'), cmd))


if __name__ == '__main__':
    main()
    if error:
        out('FAILURE', "You have failed. One or more steps failed to execute", Fore.RED)
        sys.exit(1)
    else:
        out('ALL PASS', "You rock!", Fore.GREEN)
        sys.exit(0)
