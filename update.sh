#!/bin/bash

path=`dirname $0`
git -C `dirname $0` fetch
remote_commit=`git -C $path rev-parse origin/main`
local_commit=`git -C $path rev-parse main`

if [ $remote_commit != $local_commit ]
then
	if [ $UID = 0 ]
	then
		git -C `dirname $0` pull
		cp "`dirname $0`/run_rpi_jukebox" ~/bin
		chmod +x ~/bin/run_rpi_jukebox
		source ~/.virtualenvs/rpi_jukebox/bin/activate
		pip install `dirname $0`
		deactivate
	else
		echo "please run this script as root. create one if necessary with the command:
		sudo passwd root"
	fi
else
	echo "no new updates available"
fi
