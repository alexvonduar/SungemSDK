#!/bin/bash

set -e

#----------------------------------------

# Detect brew
which -s brew
if [[ $? != 0 ]] ; then
	# Install Homebrew
	/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

brew update
brew install -y $(cat "../deps/requirements_brew.txt")

#----------------------------------------

if [ "$1" = "tuna" ] ; then
	echo "Using TUNA mirror"
	python3 -m pip install -i "https://pypi.tuna.tsinghua.edu.cn/simple" -r ../deps/requirements_macos.txt
else
	python3 -m pip install -r ../deps/requirements_macos.txt
fi
