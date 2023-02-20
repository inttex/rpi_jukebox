import logging

from rpi_jukebox.spotify_client.data_structs import Sp_Music

from rpi_jukebox.spotybox.interfaces import ControllerInterface, ViewInterface
from rpi_jukebox.spotybox.model import Model


class Controller(ControllerInterface):

    def __init__(self, view: ViewInterface, model: Model):
        self._view = view
        self._model = model

    def evaluate_rfid(self, rfid_value: int):
        self._model.evaluate_rfid(rfid_value, controller=self)

    def play_entry(self, music: Sp_Music):
        self._view.play_song(music)

    def evaluate_new_switch_state(self, new_switch_state):
        logging.info('controller, evaluating new switch state %s' % new_switch_state)

    def stop_view(self):
        logging.info('controller, stop view')
        self._view.stop_view()

    def pause_play(self):
        logging.info('controller, pause_play')
        self._view.pause_play()

    def vol_inc(self):
        logging.info('controller, vol_inc')
        self._view.vol_inc()

    def vol_dec(self):
        logging.info('controller, vol_dec')
        self._view.vol_dec()

    def stop_device(self):
        logging.info('controller, stop_device')
        self._view.stop_view()

    def stop_device_in_20min(self):
        logging.info('controller, stop_device_in_20min')
        self._view.stop_view_in20min()

    def next_track(self):
        logging.info('controller, next_track')
        self._view.next_track()

    def prev_track(self):
        logging.info('controller, prev_track')
        self._view.prev_track()
