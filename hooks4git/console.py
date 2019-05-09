# -*- coding: utf-8 -*-
from colorama import init, Fore, Back, Style
from hooks4git.tools import get_platform
import sys


class Display(object):
    color = None
    cmdbarwidth = 5

    def __init__(self, color=True):
        init()
        self.color = color

    def bareprint(self, msg):
        print(msg)

    def say(self, msg_type, msg):
        label = msg_type
        prefix = ""
        color = ""
        bgcolor = ""
        msg_color = ""
        style = ""
        msg_style = ""
        reset = ""
        if self.color is True:
            style = Style.BRIGHT
            reset = Style.RESET_ALL
            if msg_type == "FAIL":
                color = Fore.RED
            if msg_type == "SOUT":
                style = Style.DIM
                msg_style = Style.DIM
            if msg_type == "SERR":
                style = Style.DIM
                msg_style = Style.DIM
            if msg_type == "INFO":
                color = Fore.BLUE
            if msg_type == "TITLE":
                msg_color = Fore.YELLOW
                msg_style = Style.BRIGHT
            if msg_type == "WARN":
                color = Fore.YELLOW
            if msg_type in ["STEP", "STEPS", "TIME"]:
                color = Fore.BLUE
            if msg_type == "ERR!":
                color = Fore.RED
            if msg_type == "PASS":
                color = Fore.GREEN
                msg_color = Fore.GREEN
            if msg_type == "FAIL":
                color = Fore.RED
                msg_color = Fore.RED
                msg_style = Style.BRIGHT
            if msg_type == "PASS ":
                color = Fore.WHITE
                bgcolor = Back.GREEN
            if msg_type == "FAIL ":
                color = Fore.YELLOW
                bgcolor = Back.RED
        if msg_type not in ["DIV", "TITLE"]:
            prefix = label.ljust(self.cmdbarwidth) + "|" + reset + color + " "
        print(style + color + bgcolor + prefix + reset + msg_style + msg_color + msg + reset)

    def divider(self):
        dash = "-"
        if get_platform() == "Linux":
            if sys.version_info[0] < 3:
                dash = unichr(8213)  # noqa
            else:
                dash = chr(8213)
        if get_platform() == "Mac":
            if sys.version_info[0] < 3:
                dash = unichr(8212)  # noqa
            else:
                dash = chr(8212)
        if get_platform() == "Windows":  # CMD.exe
            if sys.version_info[0] < 3:
                dash = "-"
            else:
                dash = chr(8212)
        if get_platform() == "WindowsGitBash":
            if sys.version_info[0] < 3:
                dash = "-"
            else:
                dash = "-"
        self.say("DIV", dash * self.cmdbarwidth + dash + dash * (79 - 1 - self.cmdbarwidth))
