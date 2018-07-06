#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import yaml
import sys
from colorama import Fore
from colorama import Back
from colorama import Style
import datetime

# from hooks4git import __version__
__version__ = 0.1

cmdbarwidth = 5
steps_executed = 0
start_time = datetime.datetime.now()


def out(msg_type, msg, color='', bgcolor=''):
    label = msg_type
    style = Style.BRIGHT
    if msg_type == 'FAIL':
        if color == '':
            color = Fore.RED
    if msg_type == 'OUT':
        style = Style.DIM
    if msg_type == 'INFO':
        if color == '':
            color = Fore.BLUE
    if msg_type == 'WARN':
        if color == '':
            color = Fore.YELLOW
    if msg_type == 'PASS':
        if color == '':
            color = Fore.GREEN
    label = label.ljust(cmdbarwidth)
    print(style + color + bgcolor + label + '|' + Style.RESET_ALL + color + ' ' + Style.RESET_ALL + msg)


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


def execute(cmd, files, settings):
    """
    Prepare system command.
    """
    # if cmd not in ('pep8', 'flake8'):
    #     raise Exception("Unknown lint command: {}".format(cmd))
    args = settings[:]
    args.insert(0, cmd)
    args.extend(files)
    out("STEP", "$ %s" % ' '.join(args), color=Fore.BLUE)
    code, result = system(*args)
    result = result.strip().replace('\n', '\n'.ljust(cmdbarwidth + 1) + '| ')
    if len(result) < 1:
        result = 'None'
    # result = ''.ljust(cmdbarwidth)+'| ' + result + Style.RESET_ALL
    out('OUT', "%s%s%s" % (Style.DIM, result, Style.RESET_ALL))
    return code, result


# def get_changed_files():
#     """
#     Get python files from 'files to commit' git cache list.
#     """
#     files = []
#     # filelist = system('git', 'diff', '--cached', '--name-status')[1]
#     filelist = system('git', 'diff', '--name-status')[1]
#     for line in filelist:
#         try:
#             action, filename = line.strip().split()
#             if filename.endswith('.py') and action != 'D':
#                 files.append(filename)
#         except Exception as ex:  # noqa
#             pass
#     return files


def main():
    cmd = os.path.basename(__file__)
    git_root = system('git', 'rev-parse', '--show-toplevel')[1].replace('\n', '')
    configfile = "%s/.hooks4git.yml" % git_root
    try:
        with open(configfile, 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)
    except Exception as e:  # noqa
        cfg = {}

    global steps_executed
    steps_executed = 0
    no_fails = True
    try:
        cfg = cfg.get('hooks', [])
        hook = cfg.get(cmd, {'scripts': []})
        if not hook:
            hook = {'scripts': []}
        commands = hook.get('scripts', [])
        if not commands:
            commands = []
        if len(commands) > 0:
            title = "\nhooks4git v%s :: %s :: hook triggered" % (__version__, cmd.title())
            title = Fore.YELLOW + Style.BRIGHT + title + Style.RESET_ALL
            print(title)
        for command in commands:
            divider()
            steps_executed += 1
            files = []
            # if cmd == 'pre-commit':
            #     files = get_changed_files()
            result = execute(command.split()[0], files, command.split()[1:])
            if result[0] != 0:
                no_fails = False
                style = Fore.RED + Style.BRIGHT
                out('FAIL', "%s'%s' step failed to execute ✘ %s" % (style, command.split()[0], Style.RESET_ALL))
            else:
                style = Fore.GREEN
                out('PASS', "%s'%s' step executed successfully ✔ %s" % (style, command.split()[0], Style.RESET_ALL))
        return no_fails
    except Exception as e:  # noqa
        out('ERR!', str(e), color=Fore.RED)
        raise(e)


def divider():
    print('—' * cmdbarwidth + '—' + '—' * (79 - 1 - cmdbarwidth))


def report():
    if steps_executed > 0:
        divider()
        end_time = datetime.datetime.now()
        out('STEPS', '%s were executed' % steps_executed, color=Fore.BLUE)
        out('TIME', 'Execution took ' + str(end_time - start_time), color=Fore.BLUE)


if __name__ == '__main__':
    if main():
        report()
        if steps_executed > 0:
            out('PASS', "All green! Good!", Fore.WHITE, Back.GREEN)
        sys.exit(0)
    else:
        report()
        out('FAIL', "You have failed. One or more steps failed to execute.", Fore.YELLOW, Back.RED)
        sys.exit(1)
