#!/bin/bash

set -e

#--------------------

apt_raspbian_path=/etc/apt/sources.list
apt_raspberrypi_path=/etc/apt/sources.list.d/raspi.list

#--------------------

rasp_sources=raspbian.raspberrypi.org
rasp_raspi=archive.raspberrypi.org/debian

vendor_sources=mirrors.tuna.tsinghua.edu.cn/raspbian
vendor_raspi=mirrors.tuna.tsinghua.edu.cn/raspberrypi

#--------------------

if [ `grep -c $rasp_sources $apt_raspbian_path` -eq '0' ]; 
then
	echo "please replace apt sources manually at $apt_raspbian_path"
else
	echo "backup: $apt_raspbian_path.bak"
	sudo cp $apt_raspbian_path $apt_raspbian_path.bak
	echo "replace: $apt_raspbian_path"
	sudo sed -i "s|$rasp_sources|$vendor_sources|g" $apt_raspbian_path
fi

#--------------------

if [ `grep -c $rasp_raspi $apt_raspberrypi_path` -eq '0' ]; 
then
	echo "please replace apt sources manually at $apt_raspberrypi_path"
else
	echo "backup: $apt_raspberrypi_path.bak"
	sudo cp $apt_raspberrypi_path $apt_raspberrypi_path.bak
	echo "replace: $apt_raspberrypi_path"
	sudo sed -i "s|$rasp_raspi|$vendor_raspi|g" $apt_raspberrypi_path
fi
