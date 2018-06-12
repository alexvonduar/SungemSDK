#!/bin/bash

set -e

#--------------------

file_path=$(cd `dirname $0`; pwd)/../config/pip.conf
pip_dir_path="$HOME/Library/Application Support/pip"

#--------------------

if [[ ! -d "$pip_dir_path" ]]; then
   sudo mkdir -p "$pip_dir_path"
fi

#--------------------

sudo cp -i -f $file_path "$pip_dir_path"
