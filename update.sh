#!/bin/bash

path=`dirname $0`
remote_commit=`git -C $path rev-parse origin/main`
local_commit=`git -C $path rev-parse main`

if [ $remote_commit != $local_commit ]
then
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
else
	echo "no new updates available"
fi
