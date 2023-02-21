import configparser
import logging
from pathlib import Path
from queue import Queue
from threading import Thread
from time import sleep

from RPi import GPIO
from rpi_jukebox.spotify_client.data_structs import Sp_Music, SwitchState
from spotipy import Spotify, SpotifyOAuth

from rpi_jukebox.rfid_tools.rfid_thread import rfid_loop, reader_loop, switch_reader_loop
from rpi_jukebox.spotybox.interfaces import ViewInterface, ControllerInterface


class RaspiView(ViewInterface):

    # alle 10 sec abfragen, welches der aktuelle Track ist

    def __init__(self):
        self._do_terminate_threads = False
        q = Queue()
        self.rfid_thread = Thread(target=rfid_loop, args=(q, lambda: self._do_terminate_threads))
        self.reader_thread = Thread(target=reader_loop,
                                    args=(q, lambda: self._do_terminate_threads, self.rfid_callback))
        self.switch_reader_thread = Thread(target=switch_reader_loop,
                                           args=(lambda: self._do_terminate_threads, self.switch_callback))

        self._sp = self.start_spotify_connection()
        self._led_pin = 5

        self.init_LED()

    def set_controller(self, controller: ControllerInterface):
        self._controller = controller

    def rfid_callback(self, rfid_value: int):
        self._controller.evaluate_rfid(rfid_value)

    def switch_callback(self, new_switch_state:SwitchState):
        self._controller.evaluate_new_switch_state(new_switch_state)

    def run(self):
        GPIO.output(self._led_pin, GPIO.HIGH)
        self.rfid_thread.start()
        self.reader_thread.start()
        self.switch_reader_thread.start()
        try:
            while not self._do_terminate_threads:
                sleep(0.1)

        finally:
            self.rfid_thread.join()
            self.reader_thread.join()
            self.switch_reader_thread.join()
            logging.info('rfid and reader threads are successfully joined')

    def stop_view(self):
        logging.info('view: set terminate flag to True')
        self._do_terminate_threads = True
        GPIO.output(self._led_pin, GPIO.LOW)
        # GPIO.cleanup() # cleanup is done by rfid_thread

    def play_song(self, music: Sp_Music):
        logging.info('view: playing song %s' % str(music))
        self._sp.start_playback(uris=[music.sp_link, ])

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

    def init_LED(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._led_pin, GPIO.OUT)
