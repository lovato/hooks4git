# -*- coding: utf-8 -*-
import argparse
import sys
from hooks4git import __version__
from hooks4git.hook import run_trigger, hook_it


def parse_args(args):
    parser = argparse.ArgumentParser(description="Extensible Hook System for GIT")

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    parser.add_argument("-v", "--version", action="version", version="hooks4git {ver}".format(ver=__version__))
    parser.add_argument(
        "--init",
        dest="init",
        action="store_const",
        help="Install hooks4git on current repository (.git/hooks)",
        const=True,
    )
    parser.add_argument(
        "--ci",
        dest="ci",
        action="store_const",
        help="Tells hooks4git to not use colors, so output on CI will look good",
        const=True,
    )
    parser.add_argument("-t", "--trigger", dest="git_hook", help="Select which hook to trigger manually")
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])

    if args.init:
        hook_it()
    else:
        if args.git_hook:
            ci = False
            if args.ci:
                ci = True
            run_trigger(args.git_hook, ci)


if __name__ == "__main__":
    main()
