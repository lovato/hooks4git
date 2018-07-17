# hooks4git

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.org/lovato/hooks4git.svg?branch=master)](https://travis-ci.org/lovato/hooks4git)
[![Coverage Status](https://coveralls.io/repos/github/lovato/hooks4git/badge.svg?branch=master)](https://coveralls.io/github/lovato/hooks4git?branch=master)
[![PyPI version](https://badge.fury.io/py/hooks4git.svg)](https://badge.fury.io/py/hooks4git)

[![asciicast](https://asciinema.org/a/190505.png)](https://asciinema.org/a/190505)

Fully configurable language-agnostic git hooks.

Auto checks your code before you ship it. Works with any programmning language. If not, let me know.

## Availability

Production module is available from [Pypi](https://pypi.org/project/hooks4git), and development branch is also published by Travis-CI to [Pypi TestServer](https://test.pypi.org/project/hooks4git). Both are provided as EGG packages, since there is a Post Install section which creates the hook files on your local directory. Wheel packaging is not intented to do that.

Both can be downloaded and installed via the pip command.

## Getting started

These instructions will show you how to install and use the application.

### Installation

#### As a programming tool

 ```bash
 sudo pip install hooks4git
 ```

In this case, a script called `hooks4git` will be available all the time, to hook any project you are currently in.
By running this script, hooks will be applied. Please note you need to manually keep upgrading your system tools, like you do for others, like pip itself.
You probably added virtualenv and others with sudo. If in doubt, please take a look at source files.

#### As a Python project dependency

 ```bash
 pip install hooks4git --no-cache-dir
 ```

The option to not use from cache is mandatory since after download the tar.gz file, pip generates a wheel file on the cache.
Wheel files do not carry information for Post Script Installs, which is the feature that enables auto-creation of hook files. Only egg packaging supports this.

In this case, since pip doesn't recognize dev dependencies as default to be installed, the suggestion is to use it in requirements.txt file. However, this can lead to distribute this package into production environment. The solution for this is in [PipFile](https://github.com/pypa/pipfile) project.

If by any reason you already have any of the target files on your harddrive, this method will not touch those files. If you really need to update those files, you need to run `hooks4git` on the terminal, since this is the only way to interact with you asking yes or no to replace files. During egg or wheel setup, this is impossible. It is also impossible to print out information to at least tell you the tool is updating your files.

### Usage

After execution or installation, your repo is hooked for all events. Prior version used YAML for configuration management, but that caused PyYAML to be a dependency, and things went a little wrong when running it as a tool. So I choose .ini files over .json files (both have Python native parsers) because it looked less ugly.

You just need to open [.hooks4git.ini](hooks4git/.hooks4git.ini) file on the root of your project and configure it the way you want.
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

### Output

Here is a sample output for a Python configuration, with Flake8 (black and white... it has actually a full colored output):

 ```bash
hooks4git v0.1 :: Pre-Commit :: hook triggered
———————————————————————————————————————————————————————————————————————————————
STEP | $ flake8 --max-line-length=120 --exclude .git,__pycache__,build,dist
OUT  | None
PASS | 'flake8' step executed successfully
———————————————————————————————————————————————————————————————————————————————
STEPS| 1 were executed
TIME | Execution took 0:00:00.684762
PASS | All green! Good!
 ```

## Final Notes

This is supposed to run fine on Windows too, BUT windows has no native support for GIT, and this is a GIT tool, not a Python tool.
So, make sure you run this on the same command prompt you use to perform your git commands. Do not use it on `cmd.exe`.

## License

This project is licensed under MIT license. See the [LICENSE](LICENSE) file for details

## Authors

See list of [contributors](../../graphs/contributors) who participated in this project.

## Credits

- [Marco Lovato](https://github.com/lovato)
- [Collins Abitekaniza](https://github.com/collin5/precommit-hook) (where I forked from)
