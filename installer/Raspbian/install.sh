#!/bin/bash

set -e

#----------------------------------------

sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y $(cat "../deps/requirements_apt.txt")

sudo apt-get install -y build-essential pkg-config
sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev
sudo apt-get install -y libgtk2.0-dev libgtk-3-dev
sudo apt-get install -y libatlas-base-dev gfortran
sudo apt-get install -y libhdf5-dev libqtgui4 libqt4-test

#----------------------------------------

if [ "$1" = "tuna" ] ; then
    echo "Using TUNA mirror"
    TUNA="https://pypi.tuna.tsinghua.edu.cn/simple"
    python3 -m pip install -i $TUNA -r ../deps/requirements_linux.txt
    sudo -H pip3 install -i $TUNA opencv-python opencv-contrib-python
else
    # sudo bash install-opencv.sh  # install opencv from source code
    python3 -m pip install -r ../deps/requirements_linux.txt
    sudo -H pip3 install opencv-python opencv-contrib-python
fi

#----------------------------------------

sudo cp ../config/99-hornedsungem.rules /etc/udev/rules.d/
sudo chmod +x /etc/udev/rules.d/99-hornedsungem.rules
sudo udevadm control --reload
