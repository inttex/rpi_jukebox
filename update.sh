#!/bin/bash
if [ $UID = 0 ]
then
	git -C `dirname $0` pull
	source ~/.virtualenvs/rpi_jukebox/bin/activate
	pip install `dirname $0`
	echo "done! please restart"
else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi
