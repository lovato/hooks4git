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


def os_call(*args, **kwargs):
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
    except Exception as e:  # noqa
        err = str(e)
    return returncode, result_out, result_err


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
