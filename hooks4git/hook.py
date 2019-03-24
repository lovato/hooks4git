#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import configparser
import datetime
try:
    # This below only works if inside virtualenv you can still see sitepackages normally
    from hooks4git import __version__
except:  # noqa
    __version__ = 0.2

# *****************************************************************************
# https://github.com/tartley/colorama/blob/83364bf1dc2bd5a53ca9bd0154fe21d769d6f90f/colorama/ansi.py
#
# THIS FILE WAS MODIFIED FROM ORIGINAL
#
# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
#
# This module generates ANSI character codes to printing colors to terminals.
# See: http://en.wikipedia.org/wiki/ANSI_escape_code

CSI = '\033['
OSC = '\033]'
BEL = '\007'


def code_to_chars(code):
    return CSI + str(code) + 'm'


def set_title(title):
    return OSC + '2;' + title + BEL


def clear_screen(mode=2):
    return CSI + str(mode) + 'J'


def clear_line(mode=2):
    return CSI + str(mode) + 'K'


class AnsiCodes(object):
    def __init__(self):
        # the subclasses declare class attributes which are numbers.
        # Upon instantiation we define instance attributes, which are the same
        # as the class attributes but wrapped with the ANSI escape sequence
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))


class AnsiCursor(object):
    @classmethod
    def UP(cls, n=1):
        return CSI + str(n) + 'A'

    @classmethod
    def DOWN(cls, n=1):
        return CSI + str(n) + 'B'

    @classmethod
    def FORWARD(cls, n=1):
        return CSI + str(n) + 'C'

    @classmethod
    def BACK(cls, n=1):
        return CSI + str(n) + 'D'

    @classmethod
    def POS(cls, x=1, y=1):
        return CSI + str(y) + ';' + str(x) + 'H'


class AnsiFore(AnsiCodes):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX = 90
    LIGHTRED_EX = 91
    LIGHTGREEN_EX = 92
    LIGHTYELLOW_EX = 93
    LIGHTBLUE_EX = 94
    LIGHTMAGENTA_EX = 95
    LIGHTCYAN_EX = 96
    LIGHTWHITE_EX = 97


class AnsiBack(AnsiCodes):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    RESET = 49

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX = 100
    LIGHTRED_EX = 101
    LIGHTGREEN_EX = 102
    LIGHTYELLOW_EX = 103
    LIGHTBLUE_EX = 104
    LIGHTMAGENTA_EX = 105
    LIGHTCYAN_EX = 106
    LIGHTWHITE_EX = 107


class AnsiStyle(AnsiCodes):
    BRIGHT = 1
    DIM = 2   # not supported on Windows
    ITALIC = 3   # not supported on Windows
    UNDERLINE = 4   # not supported on Windows
    # BLINK = 5   # slow blink. not supported on Windows and not widely supported on Linux
    # RBLINK = 6   # rapid blink. not supported on Windows and not widely supported on Linux
    REVERSEVID = 7   # not supported on Windows
    # CONCEAL = 8   # not supported on Windows and not widely supported on Linux
    # STRIKETHROUGH = 9   # not supported on Windows and not widely supported on Linux
    # FRAKTUR = 20  # not supported on Windows and not widely supported on Linux
    NORMAL = 22
    RESET_ALL = 0


Fore = AnsiFore()
Back = AnsiBack()
Style = AnsiStyle()
Cursor = AnsiCursor()
# *****************************************************************************

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
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
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
    builtin_path = ""

    # backward compatibility to 0.1.x
    if cmd[0] == '_':
        cmd = 'scripts/' + cmd[1:]
    # end

    cmd_list = cmd.split('/')
    if cmd_list[0] == 'scripts':
        git_root = system('git', 'rev-parse', '--show-toplevel')[1].replace('\n', '')
        sys.path.insert(0, git_root)
        try:
            user_site = system('python', '-m', 'site', '--user-site')[1].replace('\n', '')
            sys.path.insert(0, user_site)
        except:  # noqa
            pass
        try:
            user_site2 = system('python2', '-m', 'site', '--user-site')[1].replace('\n', '')
            sys.path.insert(0, user_site2)
        except:  # noqa
            pass
        try:
            user_site3 = system('python3', '-m', 'site', '--user-site')[1].replace('\n', '')
            sys.path.insert(0, user_site3)
        except:  # noqa
            pass
        for path in sys.path:
            builtin_path = os.path.realpath(path + '/hooks4git/scripts/')
            ext = 'sh'  # if get_platform() in ['Linux', 'Mac', 'WindowsGitBash'] else 'bat'
            _cmd = os.path.realpath(os.path.join(builtin_path, cmd_list[1] + '.' + ext))
            if os.path.exists(_cmd):
                cmd = os.path.join(builtin_path, cmd_list[1] + '.' + ext)
                # if get_platform() == 'WindowsGitBash':
                #     cmd = '/' + cmd[0].lower() + cmd[2:].replace('\\','/')
                break

    args.insert(0, cmd)
    args.extend(files)

    display_args = args[1:]

    if builtin_path == "":
        display_cmd = args[0]
    else:
        display_cmd = args[0].replace(builtin_path, "scripts").replace('\\', '/')
        args.insert(0, 'bash')

    out("STEP", "$ %s %s" % (display_cmd, ' '.join(display_args)), color=Fore.BLUE)

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
#
#
def ini_as_dict(conf):
    d = dict(conf._sections)
    for k in d:
        d[k] = dict(conf._defaults, **d[k])
        d[k].pop('__name__', None)
    return d


def main(cmd):
    git_root = system('git', 'rev-parse', '--show-toplevel')[1].replace('\n', '')
    configfile = "%s/.hooks4git.ini" % git_root
    config = configparser.ConfigParser()
    try:
        config.read(configfile)
        cfg = ini_as_dict(config)
    except Exception as e:  # noqa
        cfg = []

    global steps_executed
    steps_executed = 0
    no_fails = True
    try:
        scripts = cfg.get('scripts', {})
        hook = cfg.get('hooks.%s.scripts' % cmd, {})
        commands = hook.keys()
        if len(commands) > 0:
            divider()
            title = "hooks4git v%s :: %s :: hook triggered" % (__version__, cmd.title())
            title = Fore.YELLOW + Style.BRIGHT + title + Style.RESET_ALL
            print(title)
        for command_item in commands:
            divider()
            steps_executed += 1
            files = []
            # if cmd == 'pre-commit':
            #     files = get_changed_files()
            command = scripts[hook[command_item]]
            result = execute(command.split()[0], files, command.split()[1:])
            if result[0] != 0:
                no_fails = False
                style = Fore.RED + Style.BRIGHT
                out('FAIL', "%s'%s/%s' step failed to execute %s" % (style, command_item, hook[command_item], Style.RESET_ALL))  # noqa
            else:
                style = Fore.GREEN
                out('PASS', "%s'%s/%s' step executed successfully %s" % (style, command_item, hook[command_item], Style.RESET_ALL))  # noqa
        return no_fails
    except Exception as e:  # noqa
        out('ERR!', str(e), color=Fore.RED)
        raise(e)


def get_platform():
    platforms = {
        'linux': 'Linux',
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'Mac',
        'win32': 'Windows',
        'win32MINGW64': 'WindowsGitBash'
    }
    platform = sys.platform + os.environ.get('MSYSTEM', '')
    if platform not in platforms:
        return sys.platform
    return platforms[platform]


def divider():
    dash = '-'
    if get_platform() == 'Linux':
        if sys.version_info[0] < 3:
            dash = unichr(8213)  # noqa
        else:
            dash = chr(8213)
    if get_platform() == 'Mac':
        if sys.version_info[0] < 3:
            dash = unichr(8212)  # noqa
        else:
            dash = chr(8212)
    if get_platform() == 'Windows':  # CMD.exe
        if sys.version_info[0] < 3:
            dash = '-'
        else:
            dash = chr(8212)
    if get_platform() == 'WindowsGitBash':
        if sys.version_info[0] < 3:
            dash = '-'
        else:
            dash = '-'
    print(dash * cmdbarwidth + dash + dash * (79 - 1 - cmdbarwidth))


def report():
    if steps_executed > 0:
        divider()
        end_time = datetime.datetime.now()
        out('STEPS', '%s were executed' % steps_executed, color=Fore.BLUE)
        out('TIME', 'Execution took ' + str(end_time - start_time), color=Fore.BLUE)


def run_trigger(cmd):
    if main(cmd):
        report()
        if steps_executed > 0:
            out('PASS', "All green! Good!", Fore.WHITE, Back.GREEN)
            divider()
        sys.exit(0)
    else:
        report()
        out('FAIL', "You have failed. One or more steps failed to execute.", Fore.YELLOW, Back.RED)
        divider()
        sys.exit(1)


if __name__ == '__main__':
    run_trigger(os.path.basename(__file__))
