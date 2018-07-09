<a href="https://asciinema.org/a/190505" target="_blank"><img src="https://asciinema.org/a/190505.png" height="400" /></a>

# hooks4git

[![Build Status](https://travis-ci.org/lovato/hooks4git.svg?branch=master)](https://travis-ci.org/lovato/hooks4git)
[![Coverage Status](https://coveralls.io/repos/github/lovato/hooks4git/badge.svg?branch=master)](https://coveralls.io/github/lovato/hooks4git?branch=master)
[![PyPI version](https://badge.fury.io/py/hooks4git.svg)](https://badge.fury.io/py/hooks4git)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Fully configurable language agnostic git hooks.

Auto checks your code before you ship it. Works with any programmning language.

## Availability

Production module is available from https://test.pypi.org/project/hooks4git/, and development branch is also published by Travis-CI to https://test.pypi.org/project/hooks4git/. Both are provided as EGG packages, since there is a Post Install section which creates the hook files on your local directory. Wheel packaging is not intented to do that.

Both can be downloaded and installed via the pip command.

## Getting started

These instructions will show you how to install and use the application.

### Installation

#### As a programming tool

 ```
 sudo pip install hooks4git
 ```

In this case, a script called `hooks4git` will be available all the time, to hook any project you are currently in.
By running this script, hooks will be applied. Please note you need to manually keep upgrading your system tools, like you do for others, like pip itself.
You probably added virtualenv and others with sudo. If in doubt, please take a look at source files.

#### As a Python project dependency

 ```
 pip install hooks4git --no-cache-dir
 ```

The option to not use from cache is mandatory since after download the tar.gz file, pip generates a wheel file on the cache.
Wheel files do not carry information for Post Script Installs, which is the feature that enables auto-creation of hook files. Only egg packaging supports this.

In this case, since pip doesn't recognize dev dependencies as default to be installed, the suggestion is to use it in requirements.txt file. However, this can lead to distribute this package into production environment. The solution for this is in https://github.com/pypa/pipfile project.

If by any reason you already have any of the target files on your harddrive, this method will not touch those files. If you really need to update those files, you need to run `hooks4git` on the terminal, since this is the only way to interact with you asking yes or no to replace files. During egg or wheel setup, this is impossible. It is also impossible to print out information to at least tell you the tool is updating your files.

### Usage

After activation, your repo is hooked for all events.

You just need to open <a href="./.hooks4git.yml">.hooks4git.yml</a> file on the root of your project and configure it the way you want.
Example section is meant for Python, but you can use any tool you want, at any given git hook event.

Example section for pre-commit, for Python:

 ```
hooks:
  pre-commit:
    scripts:
      # - echo Running "pre-commit" hook
      - flake8 --max-line-length=120 --exclude .git,__pycache__,build,dist
 ```

But it could be for NodeJS:

 ```
hooks:
  pre-commit:
    scripts:
      # - echo Running "pre-commit" hook
      - eslint server.js
      - jshint *.js
 ```

Note: All scripts you add here need to be available on your PATH for execution. So you need to make all of them depedencies on your current project, no matter the language it is written with. Per default, the available hooks are only `echo` commands, which will always pass!

### Output

Here is a sample output for a Python configuration, with Flake8 (black and white... it has actually a full colored output):

 ```
hooks4git v0.1 :: Pre-Commit :: hook triggered
———————————————————————————————————————————————————————————————————————————————
STEP | $ flake8 --max-line-length=120 --exclude .git,__pycache__,build,dist
OUT  | None
PASS | 'flake8' step executed successfully ✔
———————————————————————————————————————————————————————————————————————————————
STEPS| 1 were executed
TIME | Execution took 0:00:00.684762
PASS | All green! Good!
 ```

## License

This project is licensed under MIT license. See the <a href="./LICENSE">LICENSE</a> file for details

## Authors
See list of <a href="https://github.com/lovato/hooks4git/graphs/contributors">contributors</a> who participated in this project.

## Credits
<ul>
 <li><a href="https://github.com/lovato">Marco Lovato</a></li>
 <li><a href="https://github.com/collin5/precommit-hook">Collins Abitekaniza</a> (where I forked from)</li>
</ul>
