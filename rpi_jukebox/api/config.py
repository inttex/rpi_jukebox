import os

import xdg

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(xdg.xdg_data_home(), 'rpi_jukebox', 'musics.db')
