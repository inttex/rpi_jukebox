import os

import xdg

from rpi_jukebox.utils import tools

DATA_PATH = os.path.join(xdg.xdg_data_home(), 'rpi_jukebox')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DATA_PATH, 'musics.db')

LAST_PARAMETERS_FILE = os.path.join(DATA_PATH, 'last_parameters.json')

default_parameters = dict(
        random_stop=False,
        min_stop_time = 5,
        max_stop_time = 20,
        )

PARAMETERS = tools.load_last_parameters(default_parameters, LAST_PARAMETERS_FILE)
