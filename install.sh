#!/bin/bash
path=`dirname $0`
#apt install -y python3-dev libasound2-dev python3-venv
#python3 -m venv $HOME/venv/rpi_jukebox
source $HOME/venv/rpi_jukebox/bin/activate
pip install -e `dirname $0`
mkdir -p $HOME/.local/share/rpi_jukebox
cp "`dirname $0`/spotibox" /usr/local/bin
chmod +x /usr/local/bin/spotibox
cp "`dirname $0`/spotibox.service" /etc/systemd/system/
chmod 755 /etc/systemd/system/spotibox.service

systemctl daemon-reload
systemctl enable spotibox
systemctl start spotibox
