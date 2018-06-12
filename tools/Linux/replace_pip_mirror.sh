#!/bin/bash

set -e

#--------------------

file_path=$(cd `dirname $0`; pwd)/../config/pip.conf

pip_user_dir_path=~/.config/pip
pip_root_dir_path=/root/.config/pip

#--------------------

if [[ ! -d $pip_user_dir_path ]]; then
    sudo mkdir -p $pip_user_dir_path
fi

if [[ ! -d $pip_root_dir_path ]]; then
    sudo mkdir -p $pip_root_dir_path
fi

#--------------------

sudo cp -i -f $file_path $pip_user_dir_path
sudo cp -i -f $file_path $pip_root_dir_path