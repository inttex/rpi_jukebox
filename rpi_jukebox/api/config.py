import os

import xdg


data_path = os.path.join(xdg.xdg_data_home(), 'rpi_jukebox')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(data_path, 'musics.db')
