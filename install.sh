#!/bin/bash

if [ $UID = 0 ]
then
	mkdir -p ~/.virtualenvs
	python3 -m venv ~/.virtualenvs/rpi_jukebox
	source ~/.virtualenvs/rpi_jukebox/bin/activate
	pip install `dirname $0`
	mkdir -p $HOME/.local/share/rpi_jukebox
	create_db
	mkdir -p ~/bin
	cp "`dirname $0`/run_rpi_jukebox" ~/bin
	chmod +x ~/bin/run_rpi_jukebox
	"crontab"
else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi
