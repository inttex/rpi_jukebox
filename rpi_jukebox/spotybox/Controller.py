import logging

from rpi_jukebox.spotybox.interfaces import ControllerInterface, ViewInterface
from rpi_jukebox.spotybox.model import Model


class Controller(ControllerInterface):

    def __init__(self, view: ViewInterface, model: Model):
        self._view = view
        self._model = model

    def evaluate_rfid(self, rfid_value: int):
        def rfid_callback(uri):
            self._view.play_song(uri)

        self._model.evaluate_rfid(rfid_value, callback=rfid_callback, controller=self)

    def evaluate_new_switch_state(self, new_switch_state):
        logging.info('controller, evaluating new switch state %s' % new_switch_state)

    def stop_view(self):
        logging.info('controller, stop view')
        self._view.stop_view()

    def pause_play(self):
        logging.info('controller, pause_play')
        pass

    def vol_inc(self):
        logging.info('controller, vol_inc')
        pass

    def vol_dec(self):
        logging.info('controller, vol_dec')
        pass

    def stop_device(self):
        logging.info('controller, stop_device')
        pass

    def stop_device_in_20min(self):
        logging.info('controller, stop_device_in_20min')
        pass

    def next_track(self):
        logging.info('controller, next_track')
        # check in model, which track to play, first
        pass

    def prev_track(self):
        logging.info('controller, prev_track')
        pass
