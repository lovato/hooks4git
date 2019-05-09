# hooks4git

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.org/lovato/hooks4git.svg?branch=master)](https://travis-ci.org/lovato/hooks4git)
[![Coverage Status](https://coveralls.io/repos/github/lovato/hooks4git/badge.svg?branch=master)](https://coveralls.io/github/lovato/hooks4git?branch=master)
[![PyPI version](https://badge.fury.io/py/hooks4git.svg)](https://badge.fury.io/py/hooks4git)

[![asciicast](https://asciinema.org/a/197368.png)](https://asciinema.org/a/197368)

A fully configurable and extensible language-agnostic Hook Management System for GIT

Auto checks your code before you ship it. Works with any programmning language. If not, let me know.

## Availability

Production version is available from [Pypi](https://pypi.org/project/hooks4git), and development branch is also published by Travis-CI to [Pypi TestServer](https://test.pypi.org/project/hooks4git). Both can be downloaded and installed via the pip command.

### More information on Git Hooks

[Here](https://githooks.com). There is lots of quick information, and as well other githooks management approaches.

## Getting started

These instructions will show you how to install and use the application.

### Supported OSs

Supported OSs are Linux, MAC and Windows. However, I was not able to make it work `cmd.exe` (like if cmd.exe even works...). If you are using Windows, use it inside GitBash. **DO NOT**, I repeat, do not use it on `cmd.exe`.

### Installation

```bash
pip install hooks4git --user
```

Depending on your setup, you might want to use `pip3` instead of `pip`. Sometimes, during execution, Python2.7 complains about not finding module `configparser`. Using Python3x this doesn't happen.

Please, keep in mind that `--user` folder might not be on your PATH environment var. Usually you can find it under `~/.local/bin`. If you fix your `$PATH` now, it will be automatically fixed for any other python tool you might eventually install inside your user context.

Then, a script called `hooks4git` will be available all the time, to hook any project you are currently in. By running with the `--init` argument, hooks will be applied (i.e replace all your sample hook files).

Please note you need to manually keep upgrading your system tools, like you do for other tools, like pip itself.

### Built-in Scripts

Currently, there is only one available built-in script, called `check_branch_name.sh`. If you want to use, just follow the exemple on the default .ini file, on sub-section 'checkbranch'. This is the way to trigger built-in scripts, prefixing them with 'h4g/'.

On 0.1 release, I was using a wildcard character for built-in scripts, but that caused so many headaches, mainly when trying to make this work inside GitBash for windows (ok, that was because I was actually trying to call a bat file ... then I just gave it up). I also tried once calling 'scripts', but it may confuse with a possible local 'scripts' folder on your project.

### CLI Usage

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
flake8 = flake8 --max-line-length=119 --exclude .git,build,dist,.env,.venv
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

### CI Usage

When running inside CI, if you manage to have `hooks4git` package available, you can force trigger a hook this way:

```bash
hooks4git -t <hook> --ci
```

This will run the very same set of scrips you ran on your development workstation prior to the commit. Please note that `<hook>` is any valid entry on `.hooks4git.ini` file, not only necessarily a git-hook. See below about "Custom Hooks".

#### Colors

The `--ci` parameter tells hooks4git to not print in nice colors, just plain strings. But first check if your CI output handle colors or not. For instance, Bitbucket Pipelines handle it nicely, while Jenkins doesn't.

#### "Custom Hooks"

Hooks have those static names because they are automatically triggered by GIT. However, you can create others inside `.hooks4git.ini` file. And you can trigger them using the `-t` parameter.

So, if you like `check_branch_name` feature, you might think running it inside CI wouldn't be a great idea. How to solve it?

```bash
[hooks.ci-develop.scripts]
check = flake8
tests = tests_with_report
```

As said, there is no "ci-develop" git hook. But due to internal `hooks4git` mechanics, using `-t` flag, `hooks4git` will try to find and run that configuration.

So, it would be a matter of adding this to your CI script:

```bash
- pip install hooks4git
- hooks4git -t ci-develop
```

And since you were using flake8 and tests already on your commit and push hooks, you guarantee to run the same tools with the same parameters on CI, with a nice output, colored or not.

Disclaimer: This feature was never intended to exist, and happened to work by accident. Since it is kind of cool and doesn't break the law, I decided to document it.

### Output

Here is a sample output for a Python configuration, with Flake8 (black and white... it has actually a full colored output if --ci parameter is not issued):

```bash
———————————————————————————————————————————————————————————————————————————————
hooks4git v0.3.x :: Pre-Commit :: hook triggered
———————————————————————————————————————————————————————————————————————————————
STEP | $ flake8 --max-line-length=119 --exclude .git,__pycache__,build,dist
OUT  | None
PASS | 'flake8' step executed successfully
———————————————————————————————————————————————————————————————————————————————
STEPS| 1 were executed
TIME | Execution took 0:00:00.684762
PASS | All green! Good!
———————————————————————————————————————————————————————————————————————————————
```

## Contribute

If you are willing to code something on this project, it is quite simple. You first need to fork it directly on GitHub, so you can get a copy on your computer that you can push to. Therefore, you would be able to open a Pull Request to the original repository.

```bash
> git clone git@github.com:<super_cool_developer>/hooks4git.git
> cd hooks4git
> mkvirtualenv hooks4git -p python3  # or any way to to that
> pip install -r requirements.txt  # yes, pipenv is close
> pip install -r requirements-dev.txt
> pip uninstall hooks4git  # just in case
> pip install -e . --user
> hooks4git --init  # OF COURSE!!!
> git checkout -b feature/super_cool_feature
```

The above will install hooks4git linked to the folder you cloned the repository to, instead of the module you normally download from Pypi. This way, every change you make on the source code will affect your environment, makeing it easy to use. Of course there are several other ways, like using virtualenv, for instance. That was only a suggestion and affects all repos you have. This is the way I usually test develop versions for a few days prior to a release.

## License

This project is licensed under MIT license. See the [LICENSE](LICENSE) file for details

## Authors

See list of [contributors](../../graphs/contributors) who participated in this project.

## Credits

- [Marco Lovato](https://github.com/lovato)
- [Collins Abitekaniza](https://github.com/collin5/precommit-hook) (where I forked from)

## Change Log

### 0.4.x

- Major rework on classes and dependencies usage
- Added more tests

### 0.3.x

- Major rework on how strings are printed out
- Added --ci parameter, so no color will be printed out (Idea from [Fernando Espíndola](https://github.com/fernandoe))
- Auto create hooks folder (inside .git) if it is missing (Idea from [Édouard Lopez](https://github.com/edouard-lopez))

### 0.2.x

- Support for Windows with GitBash
- Added docker scripts for quick clean machine testing environment
- Better exception handling when user configures duplicate sections by mistake
- FIXED: Changed default max line length example to 119 instead of 120
- Replaced copying code to .git/hooks with a safe bash caller
- Replaced '\_' folder (or 'scripts' folder) with 'h4g' folder for internal scripts
- FIXED: Script order inside a hook definition was random
- Standard Error Output was not being handled and printed accordingly

### 0.1.x

- Initial release
