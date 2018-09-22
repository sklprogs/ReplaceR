#!/bin/bash

# Do not use "verbose" in order to spot errors easily

mkdir -p ./resources/locale/ru/LC_MESSAGES/
mkdir ./user

# Copy shared resources
cp -u $HOME/bin/shared/resources/{error.gif,info.gif,question.gif,warning.gif} ./resources/

# Copy other ReplaceR resources
cp -u $HOME/bin/ReplaceR/resources/locale/ru/LC_MESSAGES/replacer.mo ./resources/locale/ru/LC_MESSAGES/
cp -u $HOME/bin/ReplaceR/user/{dic,in,out}\.txt ./user/

# Copy ReplaceR Python files
cp -u $HOME/bin/ReplaceR/src/{gui,replacer}.py .

# Copy shared Python files
cp -u $HOME/bin/shared/src/{gettext_windows.py,shared.py,sharedGUI.py} .

# (Wine-only) Copy build scripts
cp -u $HOME/bin/ReplaceR/build/Wine/{build.sh,clean_up.sh,replacer.cmd,setup.py} .

ls --color=always .
