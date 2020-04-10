# -*- coding: utf-8 -*-
# from setuptools.command.install import install
import os
import sys
import shutil
import subprocess  # nosec


def copy_file(src, dest):
    try:
        shutil.copy(src, dest)
        return True
    except:  # noqa
        return False


def os_call(command):
    """
    Run system command.
    """
    command = command.strip()
    result_out = ""
    result_err = ""
    returncode = -1
    try:
        pipe1 = subprocess.PIPE
        pipe2 = subprocess.PIPE
        bash = "/bin/bash"
        shell = True

        if "Windows" in get_platform():
            bash = None
            shell = False
            if "h4g" in command:
                command = "/" + command[0].lower() + command[2:].replace(":\\", "/").replace("\\", "/")  # noqa
                command = 'c:\\Program Files\\Git\\bin\\bash.exe -c "' + command + '"'  # noqa

        proc = subprocess.Popen(command, stdout=pipe1, stderr=pipe2, shell=shell, executable=bash)  # noqa # nosec
        out, err = proc.communicate()
        try:
            tmp_out = out.decode("utf-8")
            result_out = str(tmp_out)
        except Exception as e:  # noqa # pragma: no cover
            result_out = str(out)
        try:
            tmp_err = err.decode("utf-8")
            result_err = str(tmp_err)
        except Exception as e:  # noqa # pragma: no cover
            result_err = str(err)
        returncode = proc.returncode
    except Exception as e:  # noqa # pragma: no cover
        result_err = str(e)
    return returncode, result_out, result_err


def add_usersitepackages_to_path(binary):
    try:
        user_site = os_call("%s -m site --user-site" % binary)[1].replace("\n", "")
        sys.path.insert(0, user_site)
        return user_site
    except:  # noqa # nosec # pragma: no cover
        return False


def get_platform():
    platform = sys.platform
    environ = os.environ
    platforms = {
        "linux": "Linux",
        "linux1": "Linux",
        "linux2": "Linux",
        "darwin": "Mac",
        "win32": "Windows",
        "win32MINGW64": "WindowsGitBash",
    }
    _platform = platform + environ.get("MSYSTEM", "")
    if _platform not in platforms:
        return platform
    return platforms[_platform]


def get_dash():
    dash = "-"
    if get_platform() == "Linux":
        if sys.version_info[0] < 3:
            dash = unichr(8213)  # noqa # pragma: no cover
        else:
            dash = chr(8213)
    if get_platform() == "Mac":  # pragma: no cover
        if sys.version_info[0] < 3:
            dash = unichr(8212)  # noqa
        else:
            dash = chr(8212)
    if get_platform() == "Windows":  # CMD.exe # pragma: no cover
        if sys.version_info[0] < 3:
            dash = "-"
        else:
            dash = chr(8212)
    if get_platform() == "WindowsGitBash":  # pragma: no cover
        if sys.version_info[0] < 3:
            dash = "-"
        else:
            dash = "-"
    return dash
