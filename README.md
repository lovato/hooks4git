# hooks4git

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.org/lovato/hooks4git.svg?branch=master)](https://travis-ci.org/lovato/hooks4git)
[![Coverage Status](https://coveralls.io/repos/github/lovato/hooks4git/badge.svg?branch=master)](https://coveralls.io/github/lovato/hooks4git?branch=master)
[![PyPI version](https://badge.fury.io/py/hooks4git.svg)](https://badge.fury.io/py/hooks4git)

[![asciicast](https://asciinema.org/a/197368.png)](https://asciinema.org/a/197368)

Fully configurable language-agnostic git hooks.

Auto checks your code before you ship it. Works with any programmning language. If not, let me know.

## Availability

Production module is available from [Pypi](https://pypi.org/project/hooks4git), and development branch is also published by Travis-CI to [Pypi TestServer](https://test.pypi.org/project/hooks4git). Both are provided as EGG packages, since there is a Post Install section which creates the hook files on your local directory. Wheel packaging is not intented to do that.

Both can be downloaded and installed via the pip command.

### More information on Git Hooks

[Here](https://githooks.com).

## Getting started

These instructions will show you how to install and use the application.

### Supported OSs

Supported OSs are Linux, MAC and Windows. However, I was not able to make it work CMD.exe (like if cmd.exe even works...). If you are using Windows, use it inside GitBash. DO NOT use it on `cmd.exe`.

### Installation

 ```bash
 pip3 install hooks4git --user
 ```

Depending on your setup, you might want to use `pip3` instead of `pip`.

Please, keep in mind that `--user` folder might not be on your PATH environment var. If you fix this here, it will be automatically fixed for any other python tool you might eventually install inside your user context.

In this case, a script called `hooks4git` will be available all the time, to hook any project you are currently in.
By running this script, hooks will be applied. Please note you need to manually keep upgrading your system tools, like you do for others, like pip itself.
You probably added virtualenv and others with sudo. If in doubt, please take a look at source files.

### Usage

After installation, your repo needs to be hooked for all events. Prior version used YAML for configuration management, but that caused PyYAML to be a dependency, and things went a little wrong when running it as a tool. So I choose .ini files over .json files (both have Python native parsers) because it looked less ugly.

Inside your git repository, just type:

 ```bash
hooks4git --init
 ```

And get all your regular non-sense-hard-to-use-and-hard-to-maintain-and-hard-to-share hook scripts updated.
Then, you just need to open [.hooks4git.ini](hooks4git/.hooks4git.ini) file on the root of your project and configure it the way you want.
This first example section is meant for Python, but you can use any tool you want, at any given git hook event.

Example section for pre-commit, for Python:

 ```bash
[scripts]
flake8 = flake8 --max-line-length=120 --exclude .git,build,dist,.env,.venv
nosetests = nosetests --with-coverage

[hooks.pre-commit.scripts]
check = flake8
 ```

It also could be for NodeJS:

 ```bash
[scripts]
eslint = eslint -f checkstyle index.js > checkstyle-result.xml
jshint = jshint *.js

[hooks.pre-commit.scripts]
check_a = eslint
check_b = jslint
 ```

Note: All scripts you add here need to be available on your PATH for execution. So you need to make all of them depedencies on your current project, no matter the language it is written with. Per default, the available hooks are only `echo` commands, which will always pass!

#### Built-in Scripts

Currently, there is only one available built-in script, called 'check_branch_name.sh'. If you want to use, just follow the exemple on the default .ini file, on sub-section 'checkbranch'. This is the way to trigger built-in scripts, prefixing them with 'scripts/'. On 0.1 release, I was using a '_' character for built-in scripts, but that caused so many headaches, mainly when trying to make this work inside GitBash for windows (ok, that was because I was actually trying to call a bat file ... then I gave up).

### Output

Here is a sample output for a Python configuration, with Flake8 (black and white... it has actually a full colored output):

 ```bash
———————————————————————————————————————————————————————————————————————————————
hooks4git v0.2.x :: Pre-Commit :: hook triggered
———————————————————————————————————————————————————————————————————————————————
STEP | $ flake8 --max-line-length=120 --exclude .git,__pycache__,build,dist
OUT  | None
PASS | 'flake8' step executed successfully
———————————————————————————————————————————————————————————————————————————————
STEPS| 1 were executed
TIME | Execution took 0:00:00.684762
PASS | All green! Good!
———————————————————————————————————————————————————————————————————————————————
 ```

## License

This project is licensed under MIT license. See the [LICENSE](LICENSE) file for details

## Authors

See list of [contributors](../../graphs/contributors) who participated in this project.

## Credits

- [Marco Lovato](https://github.com/lovato)
- [Collins Abitekaniza](https://github.com/collin5/precommit-hook) (where I forked from)

## Change Log

### 0.2.x

- Support for Windows with GitBash
- Added docker scripts for quick clean machine testing environment

### 0.1.x

- Initial release