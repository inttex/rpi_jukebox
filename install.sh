#!/bin/bash
path=`dirname $0`
#if [ $UID = 0 ]
#then
apt install -y python3-dev libasound2-dev python3-venv
python3 -m venv $HOME/venv/rpi_jukebox
source $HOME/venv/rpi_jukebox/bin/activate
pip install -e `dirname $0`
mkdir -p $HOME/.local/share/rpi_jukebox
	#create_db
	#cp "`dirname $0`/jukebox_server" /usr/local/bin
	#chmod +x /usr/local/bin/jukebox_server
	#cp "`dirname $0`/jukebox_client" /usr/local/bin
	#chmod +x /usr/local/bin/jukebox_client
	#$path/create_update_shortcut.sh
	#cp "`dirname $0`/jukebox_client.service" /etc/systemd/system/
	#chmod 755 /etc/systemd/system/jukebox_client.service
	#cp "`dirname $0`/jukebox_server.service" /etc/systemd/system/
	#chmod 755 /etc/systemd/system/jukebox_server.service
	#systemctl daemon-reload
	#systemctl enable jukebox_server
	#systemctl enable jukebox_client
	#systemctl start jukebox_client
	#systemctl start jukebox_server
#else
	#echo "please run this script as root. create one if necessary with the command:
	#sudo passwd root"
#fi
