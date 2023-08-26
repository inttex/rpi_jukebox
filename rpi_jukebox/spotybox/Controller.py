import logging

from rpi_jukebox.spotify_client.data_structs import SwitchState

from rpi_jukebox.spotybox.interfaces import ControllerInterface, ViewInterface
from rpi_jukebox.spotybox.model import Model


class Controller(ControllerInterface):

    def __init__(self, view: ViewInterface, model: Model):
        self._view = view
        self._model = model

    def evaluate_rfid(self, rfid_value: int):
        self._model.evaluate_rfid(rfid_value, controller=self)

    def evaluate_new_switch_state(self, new_switch_state: SwitchState):
        self._model.set_switch_state(new_switch_state)
        logging.info('controller, evaluating new switch state %s' % new_switch_state)

    def stop_view(self):
        logging.info('controller, stop view')
        self._view.stop_view()
        logging.info('controller, stop model')
        self._model.stop_model()

    def stop_device(self):
        logging.info('controller, stop_device')
        self._view.stop_view()

    def stop_device_in_20min(self):
        logging.info('controller, stop_device_in_20min')
        self._model.stop_view_in20min()
