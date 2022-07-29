#!/bin/bash

path=`dirname $0`
if [ $UID = 0 ]
then
	mkdir -p ~/.virtualenvs
	python3 -m venv /usr/local/bin/rpi_jukebox
	source /usr/local/bin/rpi_jukebox/bin/activate
	pip install `dirname $0`
	mkdir -p $HOME/.local/share/rpi_jukebox
	create_db
	cp "`dirname $0`/run_rpi_jukebox" /usr/local/bin
	chmod +x /usr/local/bin/run_rpi_jukebox
	$path/create_update_shortcut.sh
	crontab -l > tempfile
	echo "@reboot run_rpi_jukebox" >> tempfile
	crontab tempfile
	rm tempfile
else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi
