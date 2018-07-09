#!/bin/bash

set -e

#----------------------------------------

sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y $(cat "../deps/requirements_apt.txt")

#----------------------------------------

if [[ `lsb_release -rs` == "14.04" ]] ; then
    sudo -H pip3 install --upgrade pip
fi

if [ "$1" = "tuna" ] ; then
    echo "Using TUNA mirror"
    TUNA="https://pypi.tuna.tsinghua.edu.cn/simple"
    sudo -H python3 -m pip install -i $TUNA -r ../deps/requirements_linux.txt
else
    sudo -H python3 -m pip install -r ../deps/requirements_linux.txt
fi

#----------------------------------------

bash install-opencv.sh

#----------------------------------------

sudo cp ../config/99-hornedsungem.rules /etc/udev/rules.d/
sudo chmod +x /etc/udev/rules.d/99-hornedsungem.rules
sudo udevadm control --reload
