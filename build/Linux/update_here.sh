#!/bin/sh

# Do not use "verbose" in order to spot errors easily

mkdir -p ./resources/locale/ru/LC_MESSAGES/
mkdir ./user

# Copy shared resources
cp -u /usr/local/bin/shared/resources/{error.gif,info.gif,question.gif,warning.gif} ./resources/

# Copy other ReplaceR resources
cp -u /usr/local/bin/ReplaceR/resources/locale/ru/LC_MESSAGES/replacer.mo ./resources/locale/ru/LC_MESSAGES/
cp -u /usr/local/bin/ReplaceR/user/{dic,in,out}\.txt ./user/

# Copy ReplaceR Python files
cp -u /usr/local/bin/ReplaceR/src/{gui,replacer}.py .

# Copy shared Python files
cp -u /usr/local/bin/shared/src/{gettext_windows.py,shared.py,sharedGUI.py} .

# (Linux-only) Copy build scripts
cp -u /usr/local/bin/ReplaceR/build/Linux/{build.sh,clean_up.sh,setup.py} .

ls .
