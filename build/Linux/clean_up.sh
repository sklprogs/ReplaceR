#!/bin/bash

# Do not use "verbose" in order to spot errors easily

# Remove shared resources
rm -f ./resources/{error.gif,info.gif,question.gif,warning.gif}

# Remove other ReplaceR resources
rm -f ./resources/locale/ru/LC_MESSAGES/replacer.mo
rm -f ./user/{dic,in,out}\.txt

# Remove ReplaceR Python files
rm -f ./{gui,replacer}.py

# Remove shared Python files
rm -f ./{gettext_windows.py,shared.py,sharedGUI.py}

# (Linux-only) Remove build scripts
rm -f ./{build.sh,clean_up.sh,setup.py}

rmdir -p resources/locale/ru/LC_MESSAGES user

ls --color=always .
