# -*- coding: utf-8 -*-
import os
import sys
import configparser
import datetime
from hooks4git import __version__
from hooks4git.tools import oscall, copy_file
from hooks4git.console import Display

steps_executed = 0
start_time = datetime.datetime.now()
display = None


def get_hooks_path(git_root_path):
    if git_root_path is None:
        msg = "I am afraid I can't to that. You are not inside a GIT repo. Reach one and re-run this tool."
        Display.bareprint(msg)
        return None
    if git_root_path.endswith("/.git") is False:
        msg = "Humm, this is odd. Your GIT repo must have a .git folder. Looks like you are not inside a GIT repo."
        Display.bareprint(msg)
        return None
    hooks_path = os.path.join(git_root_path, "hooks")
    if not os.path.isdir(hooks_path):
        message = "Looks like your '.git/hooks' folder is missing."
        Display.bareprint("%s Let's try to fix this..." % message)
        try:
            os.makedirs(hooks_path)
            Display.bareprint("Cool! '.git/hooks' folder was created.")
            return hooks_path
        except:  # noqa
            return None
    else:
        return hooks_path


def hook_it(path=os.environ["PWD"]):
    # setup_path = os.path.join(oscall('git', 'rev-parse', '--show-toplevel')[1].replace('\n', ''), 'hooks4git')
    setup_path = os.path.dirname(os.path.realpath(__file__))
    try:
        path = oscall("git", "-C", path, "rev-parse", "--show-toplevel")[1].replace("\n", "")
        git_path = oscall("git", "-C", path, "rev-parse", "--git-dir")[1].replace("\n", "")
        if git_path == ".git":
            git_path = os.path.join(path, git_path)
    except:  # noqa
        git_path = None

    path = os.path.abspath(path)
    setup_path = os.path.abspath(setup_path)
    hooks_path = get_hooks_path(git_path)
    if hooks_path:
        origin_config = os.path.join(setup_path, ".hooks4git.ini")
        target_config = os.path.join(path, ".hooks4git.ini")
        if os.path.isfile(target_config):
            target_config = target_config.replace(".ini", "-" + __version__ + ".ini")
        copy_file(origin_config, target_config)
        files_to_copy = oscall("ls", os.path.join(setup_path, "git/hooks"))
        for file in files_to_copy[1].split("\n"):
            if file not in ["__pycache__", "", "hooks4git.py"]:
                src = os.path.join(setup_path, "git/hooks", file)
                target = os.path.join(git_path, "hooks", file)
                copy_file(src, target)
        Display.bareprint("Wow! hooks4git files were installed successfully! Thanks for hooking!")
        Display.bareprint("If you are a courious person, take a look at .git/hooks folder.")
        Display.bareprint("TIP: To get rid of hooks, comment lines on the .hooks4git.ini file.")
    return True


def execute(cmd, files, settings):
    """
    Prepare system command.
    """
    args = settings[:]
    builtin_path = ""

    # backward compatibility to 0.1.x
    if cmd[0] == "_":
        cmd = "h4g/" + cmd[1:]
        display.say("WARN", "Please upgrade your ini file to call built in scripts prefixed by 'h4g/'")
    # backward compatibility to early 0.2.x
    if cmd[0:8] == "scripts/":
        cmd = "h4g/" + cmd[8:]
        display.say("WARN", "Please upgrade your ini file to call built in scripts prefixed by 'h4g/'")
    # end

    cmd_list = cmd.split("/")
    git_root = oscall("git", "rev-parse", "--show-toplevel")[1].replace("\n", "")
    if cmd_list[0] == "h4g":
        sys.path.insert(0, git_root)
        try:
            user_site = oscall("python", "-m", "site", "--user-site")[1].replace("\n", "")
            sys.path.insert(0, user_site)
        except:  # noqa # nosec
            pass
        try:
            user_site2 = oscall("python2", "-m", "site", "--user-site")[1].replace("\n", "")
            sys.path.insert(0, user_site2)
        except:  # noqa # nosec
            pass
        try:
            user_site3 = oscall("python3", "-m", "site", "--user-site")[1].replace("\n", "")
            sys.path.insert(0, user_site3)
        except:  # noqa # nosec
            pass
        for path in sys.path:
            builtin_path = os.path.realpath(path + "/hooks4git/h4g/")
            _cmd = os.path.realpath(os.path.join(builtin_path, cmd_list[1]))
            if os.path.exists(_cmd):
                cmd = os.path.join(builtin_path, cmd_list[1])
                break

    args.insert(0, cmd)

    display_args = args[1:]

    if builtin_path == "":
        display_cmd = args[0]
    else:
        display_cmd = args[0].replace(builtin_path, "h4g").replace("\\", "/")
        args.insert(0, "bash")

    display_message = "%s %s" % (display_cmd, " ".join(display_args))

    if cmd == "echo":
        if files:
            _arg = "--filename=%s" % ",".join(files)
            args.append(_arg)
            display_message += " " + _arg.replace(git_root, ".")[: (66 - len(display_message))] + "..."

    display.say("STEP", "$ %s" % display_message)

    code, result, err = oscall(*args)
    result = result.strip().replace("\n", "\n".ljust(display.cmdbarwidth + 1) + "| ")
    err = err.strip().replace("\n", "\n".ljust(display.cmdbarwidth + 1) + "| ")
    if len(result) > 0:
        display.say("SOUT", result)
    if len(err) > 0:
        display.say("SERR", err)
    return code, result, err


def main(cmd):
    git_root = oscall("git", "rev-parse", "--show-toplevel")[1].replace("\n", "")
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
        scripts = cfg.get("scripts", {})
        hook = cfg.get("hooks.%s.scripts" % cmd, {})
        commands = hook.keys()
        # If section is ommited, app outputs absolutelly nothing to stdout
        if "hooks." + cmd.lower() + ".scripts" in config.sections():
            display.divider()
            title = "hooks4git v%s :: %s :: hook triggered" % (__version__, cmd.title())
            display.say("TITLE", title)
            if len(exception_message) > 0:
                display.divider()
                Display.bareprint("Oops! " + exception_message)
                display.divider()
                exit(1)
            display.divider()
            for command_item in commands:
                steps_executed += 1
                files = []
                # files = get_changed_files()
                command = scripts[hook[command_item]]
                result = execute(command.split()[0], files, command.split()[1:])
                if result[0] != 0:
                    no_fails = False
                    display.say("FAIL", "'%s/%s' step failed to execute" % (command_item, hook[command_item]))  # noqa
                else:
                    display.say(
                        "PASS", "'%s/%s' step executed successfully" % (command_item, hook[command_item])
                    )  # noqa
                display.divider()
        return no_fails
    except Exception as e:  # noqa
        display.say("ERR!", str(e))
        raise (e)


def report():
    if steps_executed > 0:
        end_time = datetime.datetime.now()
        if steps_executed > 1:
            to_be = "were"
        else:
            to_be = "was"
        display.say("STEPS", "%s %s executed" % (steps_executed, to_be))
        display.say("TIME", "Execution took " + str(end_time - start_time))


def run_trigger(cmd, ci=False):
    color_flag = not ci
    global display
    display = Display(color_flag)

    if main(cmd):
        report()
        if steps_executed > 0:
            display.say("PASS ", "All green! Good!")
            display.divider()
        sys.exit(0)
    else:
        report()
        display.say("FAIL ", "You have failed. One or more steps failed to execute.")
        display.divider()
        sys.exit(1)
