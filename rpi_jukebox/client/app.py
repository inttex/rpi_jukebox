import logging


from rpi_jukebox.client.models import MusicLoader, APICommunicator
from rpi_jukebox.client.views import JukeboxView
from rpi_jukebox.client.controllers import JukeboxController
from rpi_jukebox.api.config import CLIENT_LOG_FILE


logging.basicConfig(filename=CLIENT_LOG_FILE, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def main():
    HOST = 'http://localhost:43210/'
    run_jukebox_client(HOST)


def run_jukebox_client(host):
    app = JukeboxApp(host)
    app.run()


class JukeboxApp():

    def __init__(self, host):
        music_loader = MusicLoader() # gets wav and prepares start times
        api_communicator = APICommunicator(host) #communicates by requests to the api restless server
        self._view = JukeboxView() # get input from RFID, play and stop play_buffer
        controller = JukeboxController(api_communicator, music_loader, self._view) # gets RFID, requests song via
        # APICommunicator and pays sond in _view

        self._view.set_controller(controller)

    def run(self):
        logging.info('start the client')
        self._view.run()


if __name__ == '__main__':
    main()
