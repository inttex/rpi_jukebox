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
		cp "`dirname $0`/jukebox_server" /usr/local/bin
		chmod +x /usr/local/bin/jukebox_server
		cp "`dirname $0`/jukebox_client" /usr/local/bin
		chmod +x /usr/local/bin/jukebox_client
		source /usr/local/bin/rpi_jukebox/bin/activate
		pip install `dirname $0`
		deactivate
		systemctl restart jukebox_client
	else
		echo "please run this script as root. create one if necessary with the command:
		sudo passwd root"
	fi
else
	echo "no new updates available"
fi
