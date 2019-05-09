# -*- coding: utf-8 -*-
import os
import subprocess  # nosec
import sys
import configparser
import datetime
from colorama import init, Fore, Back, Style
from hooks4git import __version__

init()
cmdbarwidth = 5
steps_executed = 0
start_time = datetime.datetime.now()
ci_output = False


def out(msg_type, msg):
    label = msg_type
    prefix = ""
    color = ""
    bgcolor = ""
    msg_color = ""
    style = ""
    msg_style = ""
    reset = ""
    if ci_output is not True:
        style = Style.BRIGHT
        reset = Style.RESET_ALL
        if msg_type == 'FAIL':
            color = Fore.RED
        if msg_type == 'SOUT':
            style = Style.DIM
            msg_style = Style.DIM
        if msg_type == 'SERR':
            style = Style.DIM
            msg_style = Style.DIM
        if msg_type == 'INFO':
            color = Fore.BLUE
        if msg_type == 'TITLE':
            msg_color = Fore.YELLOW
            msg_style = Style.BRIGHT
        if msg_type == 'WARN':
            color = Fore.YELLOW
        if msg_type in ['STEP', 'STEPS', 'TIME']:
            color = Fore.BLUE
        if msg_type == 'ERR!':
            color = Fore.RED
        if msg_type == 'PASS':
            color = Fore.GREEN
            msg_color = Fore.GREEN
        if msg_type == 'FAIL':
            color = Fore.RED
            msg_color = Fore.RED
            msg_style = Style.BRIGHT
        if msg_type == 'PASS ':
            color = Fore.WHITE
            bgcolor = Back.GREEN
        if msg_type == 'FAIL ':
            color = Fore.YELLOW
            bgcolor = Back.RED
    if msg_type not in ['DIV', 'TITLE']:
        prefix = label.ljust(cmdbarwidth) + '|' + reset + color + ' '
    print(style + color + bgcolor + prefix + reset + msg_style + msg_color + msg + reset)


def system(*args, **kwargs):
    """
    Run system command.
    """
    result_out = ""
    result_err = ""
    returncode = -1
    try:
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # nosec
        out, err = proc.communicate()
        try:
            tmp_out = out.decode('utf-8')
            result_out = str(tmp_out)
        except Exception as e:  # noqa
            result_out = str(out)
        try:
            tmp_err = err.decode('utf-8')
            result_err = str(tmp_err)
        except Exception as e:  # noqa
            result_err = str(err)
        returncode = proc.returncode
    except Exception as e:  # noqa
        err = str(e)
    return returncode, result_out, result_err


def execute(cmd, files, settings):
    """
    Prepare system command.
    """
    args = settings[:]
    builtin_path = ""

    # backward compatibility to 0.1.x
    if cmd[0] == '_':
        cmd = 'h4g/' + cmd[1:]
        out('WARN', "Please upgrade your ini file to call built in scripts prefixed by 'h4g/'")
    # backward compatibility to early 0.2.x
    if cmd[0:8] == 'scripts/':
        cmd = 'h4g/' + cmd[8:]
        out('WARN', "Please upgrade your ini file to call built in scripts prefixed by 'h4g/'")
    # end

    cmd_list = cmd.split('/')
    git_root = system('git', 'rev-parse', '--show-toplevel')[1].replace('\n', '')
    if cmd_list[0] == 'h4g':
        sys.path.insert(0, git_root)
        try:
            user_site = system('python', '-m', 'site', '--user-site')[1].replace('\n', '')
            sys.path.insert(0, user_site)
        except:  # noqa # nosec
            pass
        try:
            user_site2 = system('python2', '-m', 'site', '--user-site')[1].replace('\n', '')
            sys.path.insert(0, user_site2)
        except:  # noqa # nosec
            pass
        try:
            user_site3 = system('python3', '-m', 'site', '--user-site')[1].replace('\n', '')
            sys.path.insert(0, user_site3)
        except:  # noqa # nosec
            pass
        for path in sys.path:
            builtin_path = os.path.realpath(path + '/hooks4git/h4g/')
            _cmd = os.path.realpath(os.path.join(builtin_path, cmd_list[1]))
            if os.path.exists(_cmd):
                cmd = os.path.join(builtin_path, cmd_list[1])
                break

    args.insert(0, cmd)

    display_args = args[1:]

    if builtin_path == "":
        display_cmd = args[0]
    else:
        display_cmd = args[0].replace(builtin_path, "h4g").replace('\\', '/')
        args.insert(0, 'bash')

    display_message = "%s %s" % (display_cmd, ' '.join(display_args))

    if cmd == 'echo':
        if files:
            _arg = '--filename=%s' % ','.join(files)
            args.append(_arg)
            display_message += " " + _arg.replace(git_root, ".")[:(66 - len(display_message))] + "..."

    out("STEP", "$ %s" % display_message)

    code, result, err = system(*args)
    result = result.strip().replace('\n', '\n'.ljust(cmdbarwidth + 1) + '| ')
    err = err.strip().replace('\n', '\n'.ljust(cmdbarwidth + 1) + '| ')
    if len(result) > 0:
        out('SOUT', result)
    if len(err) > 0:
        out('SERR', err)
    return code, result, err


def main(cmd):
    git_root = system('git', 'rev-parse', '--show-toplevel')[1].replace('\n', '')
    configfile = "%s/.hooks4git.ini" % git_root
    config = configparser.ConfigParser()
    cfg = {}
    exception_message = ""
    try:
        config.read(configfile)
        cfg = dict(config._sections)
    except Exception as e:  # noqa
        exception_message = str(e)

    global steps_executed
    steps_executed = 0
    no_fails = True
    try:
        scripts = cfg.get('scripts', {})
        hook = cfg.get('hooks.%s.scripts' % cmd, {})
        commands = hook.keys()
        # If section is ommited, app outputs absolutelly nothing to stdout
        if 'hooks.'+cmd.lower()+'.scripts' in config.sections():
            divider()
            title = "hooks4git v%s :: %s :: hook triggered" % (__version__, cmd.title())
            out('TITLE', title)
            # if len(commands) == 0:
            #     print("Somehow, nothing to do...")
            if len(exception_message) > 0:
                divider()
                print("Oops! " + exception_message)
                divider()
                exit(1)
            divider()
            for command_item in commands:
                steps_executed += 1
                files = []
                # files = get_changed_files()
                command = scripts[hook[command_item]]
                result = execute(command.split()[0], files, command.split()[1:])
                if result[0] != 0:
                    no_fails = False
                    out('FAIL', "'%s/%s' step failed to execute" % (command_item, hook[command_item]))  # noqa
                else:
                    out('PASS', "'%s/%s' step executed successfully" % (command_item, hook[command_item]))  # noqa
                divider()
        return no_fails
    except Exception as e:  # noqa
        out('ERR!', str(e))
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
    out('DIV', dash * cmdbarwidth + dash + dash * (79 - 1 - cmdbarwidth))


def report():
    if steps_executed > 0:
        end_time = datetime.datetime.now()
        if steps_executed > 1:
            to_be = 'were'
        else:
            to_be = 'was'
        out('STEPS', '%s %s executed' % (steps_executed, to_be))
        out('TIME', 'Execution took ' + str(end_time - start_time))


def run_trigger(cmd, ci=False):
    global ci_output
    ci_output = ci
    if main(cmd):
        report()
        if steps_executed > 0:
            out('PASS ', "All green! Good!")
            divider()
        sys.exit(0)
    else:
        report()
        out('FAIL ', "You have failed. One or more steps failed to execute.")
        divider()
        sys.exit(1)
