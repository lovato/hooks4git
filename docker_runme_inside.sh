#!/bin/bash
echo INSTALLING from local folder /tmp/hooks4git
echo
cd /tmp
pip install /tmp/hooks4git
echo
mkdir /tmp/hooks4git_workdir
cp -r /tmp/hooks4git /tmp/hooks4git_workdir
cd /tmp/hooks4git_workdir
rm -rf .git
echo GIT INIT
git init
echo
echo HOOKS4GIT INIT
hooks4git --init
echo
echo HOOKS4GIT -v
hooks4git -v
echo
echo HOOKS4GIT -h
hooks4git -h
echo
echo HOOKS4GIT -t
hooks4git -t pre-commit
