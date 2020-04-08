#!/bin/bash

if [ -z "$1" ]
then
    valid='^(feature|bugfix|hotfix)\/.+'
else
    valid="$1"
fi

# branch=`git rev-parse --abbrev-ref HEAD`
# branch=`git symbolic-ref --short HEAD`  # https://stackoverflow.com/questions/6245570/how-to-get-the-current-branch-name-in-git
branch=$(git status | head -1 | sed -n '/On branch /s///p')

if [[ $branch =~ $valid ]]; then
    echo Branch is OK with naming conventions
else
    echo Your branch \'$branch\' needs a better name to match conventions. Sorry.
    echo This rules branch naming: $valid
    echo You can try a few at https://regex101.com/
    echo Then, please, follow these steps if needed:
    echo - http://tinyurl.com/renamegitbranches
    exit 1
fi
