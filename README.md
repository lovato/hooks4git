# hooks4git

[![Build Status](https://travis-ci.org/lovato/hooks4git.svg?branch=master)](https://travis-ci.org/lovato/hooks4git)
[![Coverage Status](https://coveralls.io/repos/github/lovato/hooks4git/badge.svg?branch=master)](https://coveralls.io/github/lovato/hooks4git?branch=master)
[![PyPI version](https://badge.fury.io/py/hooks4git.svg)](https://badge.fury.io/py/hooks4git)

Fully configurable language agnostic git hooks.
Auto checks your code before you ship it. Works with any programmning language.

## Availability
Production module is available from https://test.pypi.org/project/hooks4git/, and development branch is also published by Travis-CI to https://test.pypi.org/project/hooks4git/. Both are provided as EGG packages, since there is a Post Install section which creates the hook files on your local directory. Wheel packaging is not intented to do that.

Both can be downloaded and installed via the pip command.

## Getting started
These instructions will show you how to install and use the application.

### Installation
 ```
 pip install hooks4git
 ```

### Usage
After you install the package, your repo is automatically hooked for all events.
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

### Output
Here is a sample output (black and white... it has actually a full colored output):
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
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under MIT license. See the <a href="./LICENSE">LICENSE</a> file for details

## Authors
See list of <a href="https://github.com/lovato/hooks4git/graphs/contributors">contributors</a> who participated in this project.

## Credits
<ul>
 <li><a href="https://github.com/lovato">Marco Lovato</a></li>
 <li><a href="https://github.com/collin5">Collins Abitekaniza</a> (where I forked from)</li>
 <li><a href="https://github.com/andela-engmkwalusimbi">Walusimbi Mahad</a></li>
</ul>
