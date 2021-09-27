#!/bin/bash

if [ $UID = 0 ]
then
	mkdir -p ~/.virtualenvs
	python3 -m venv ~/.virtualenvs/rpi_jukebox
	source ~/.virtualenvs/rpi_jukebox/bin/activate
	pip install `dirname $0`
else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi
#-create .local/rpi_jukebox
#-create db
