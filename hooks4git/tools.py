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


def oscall(*args, **kwargs):
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
        except Exception as e:  # noqa
            result_out = str(out)
        try:
            tmp_err = err.decode("utf-8")
            result_err = str(tmp_err)
        except Exception as e:  # noqa
            result_err = str(err)
        returncode = proc.returncode
    except Exception as e:  # noqa
        err = str(e)
    return returncode, result_out, result_err


def get_platform():
    platforms = {
        "linux": "Linux",
        "linux1": "Linux",
        "linux2": "Linux",
        "darwin": "Mac",
        "win32": "Windows",
        "win32MINGW64": "WindowsGitBash",
    }
    platform = sys.platform + os.environ.get("MSYSTEM", "")
    if platform not in platforms:
        return sys.platform
    return platforms[platform]
