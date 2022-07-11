#/bin/bash

path=`dirname $0`
echo "#!/bin/bash" > ~/bin/update_rpi_jukebox
echo `realpath $path/update.sh` >> ~/bin/update_rpi_jukebox
chmod +x ~/bin/update_rpi_jukebox
