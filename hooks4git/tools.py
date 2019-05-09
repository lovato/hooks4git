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


def get_hooks_path(git_root_path):
    if git_root_path is None:
        print("I am afraid I can't to that. You are not inside a GIT repo. Reach one and re-run this tool.")
        return None
    if git_root_path.endswith("/.git") is False:
        print(
            "Humm, this is odd. Your GIT repo must have a .git folder. Looks like you are not inside a GIT repo."
        )  # noqa
        return None
    hooks_path = os.path.join(git_root_path, "hooks")
    if not os.path.isdir(hooks_path):
        message = "Looks like your '.git/hooks' folder is missing."
        print("%s Let's try to fix this..." % message)
        try:
            os.makedirs(hooks_path)
            print("Cool! '.git/hooks' folder was created.")
            return hooks_path
        except:  # noqa
            return None
    else:
        return hooks_path


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
