#/bin/bash

path=`dirname $0`
echo "#!/bin/bash" > /usr/local/bin/update_rpi_jukebox
echo "`realpath $path/update.sh` > /root/.local/share/rpi_jukebox/last_update_log 2>&1" >> /usr/local/bin/update_rpi_jukebox
chmod +x /usr/local/bin/update_rpi_jukebox
