import logging
import sys

from rpi_jukebox.spotybox.Controller import Controller
from rpi_jukebox.spotybox.View import View
from rpi_jukebox.spotybox.config import CLIENT_LOG_FILE
from rpi_jukebox.spotybox.model import Model

logging.basicConfig(filename=CLIENT_LOG_FILE, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def main():
    app = RaspyBoxApp()
    app.run()


class RaspyBoxApp():

    def __init__(self):
        # instantiate model components
        self._model = Model()
        # music_loader = MusicLoader() # gets wav and prepares start times
        # api_communicator = APICommunicator(host) #communicates by requests to the api restless server

        # view and controller
        self._view = View()  # get input from RFID, play and stop play_buffer
        controller = Controller(self._view, self._model)  # gets RFID, requests song via
        self._view.set_controller(controller)

    def run(self):
        logging.info('start view')
        self._view.run()


if __name__ == '__main__':
    main()
