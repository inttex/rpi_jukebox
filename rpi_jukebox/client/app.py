import logging


from rpi_jukebox.client.models import MusicLoader, APICommunicator
from rpi_jukebox.client.views import JukeboxView
from rpi_jukebox.client.controllers import JukeboxController
from rpi_jukebox.api.config import CLIENT_LOG_FILE


logging.basicConfig(filename=CLIENT_LOG_FILE, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def main():
    HOST = 'http://localhost:5000/'
    run_jukebox_client(HOST)


def run_jukebox_client(host):
    app = JukeboxApp(host)
    app.run()


class JukeboxApp():

    def __init__(self, host):
        music_loader = MusicLoader()
        api_communicator = APICommunicator(host)
        self._view = JukeboxView()
        controller = JukeboxController(api_communicator, music_loader, self._view)
        self._view.set_controller(controller)

    def run(self):
        logging.info('start the client')
        self._view.run()


if __name__ == '__main__':
    main()
