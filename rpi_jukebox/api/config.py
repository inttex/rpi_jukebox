import os

import xdg


DATA_PATH = os.path.join(xdg.xdg_data_home(), 'rpi_jukebox')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DATA_PATH, 'musics.db')
