#/bin/bash

path=`dirname $0`
echo "#!/bin/bash" > ~/bin/update_rpi_jukebox
echo "`realpath $path/update.sh` > /root/.local/share/rpi_jukebox/last_update_log 2>&1" >> ~/bin/update_rpi_jukebox
chmod +x ~/bin/update_rpi_jukebox
