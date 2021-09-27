#!/bin/bash

if [ $UID = 0 ]
then
	echo
else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi
#-create virtual env python3
#-activate env
#-pip install .
#-create .local/rpi_jukebox
#-create db
