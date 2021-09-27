#!/bin/bash

if [ $UID = 0 ]
then
	mkdir -p ~/.virtualenvs
	python3 -m venv ~/.virtualenvs/rpi_jukebox
else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi
#-activate env
#-pip install .
#-create .local/rpi_jukebox
#-create db
