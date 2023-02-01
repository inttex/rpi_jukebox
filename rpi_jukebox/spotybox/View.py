import configparser
import logging
from pathlib import Path
from queue import Queue
from threading import Thread
from time import sleep

from spotipy import Spotify, SpotifyOAuth

from rpi_jukebox.rfid_tools.rfid_thread import rfid_loop, reader_loop
from rpi_jukebox.spotybox.interfaces import ViewInterface, ControllerInterface


class View(ViewInterface):

    def __init__(self):
        self._do_terminate_threads = False
        q = Queue()
        self.rfid_thread = Thread(target=rfid_loop, args=(q, lambda: self._do_terminate_threads))
        self.reader_thread = Thread(target=reader_loop,
                                    args=(q, lambda: self._do_terminate_threads, self.rfid_callback))

        self._sp = self.start_spotify_connection()

    def set_controller(self, controller: ControllerInterface):
        self._controller = controller

    def rfid_callback(self, rfid_value: int):
        self._controller.evaluate_rfid(rfid_value)

    def run(self):
        self.rfid_thread.start()
        self.reader_thread.start()
        try:
            while not self._do_terminate_threads:
                sleep(0.1)

        finally:
            logging.info('terminating rfid and reader threads')
            self.rfid_thread.join()
            self.reader_thread.join()
            logging.info('terminating rfid and reader threads --> done')

    def stop_view(self):
        logging.info('view: set terminate flag to True')
        self._do_terminate_threads=True

    def play_song(self, uri):
        logging.info('view: playing song %s' % uri)
        self._sp.start_playback(uri)

    def start_spotify_connection(self):
        config = configparser.ConfigParser()
        configfile = Path(r'../../res/config.cfg')
        config.read(configfile)
        username = config['SPOTIFY']['username']
        clientID = config['SPOTIFY']['clientID']
        clientSecret = config['SPOTIFY']['clientSecret']
        redirect_uri = config['SPOTIFY']['redirect_uri']
        self._DEVICE_ID = config['SPOTIFY']['DEVICE_ID_LINUX']

        sp = Spotify(auth_manager=SpotifyOAuth(username=username,
                                               client_id=clientID,
                                               client_secret=clientSecret,
                                               redirect_uri=redirect_uri,
                                               scope="user-read-playback-state,user-modify-playback-state"))
        return sp
