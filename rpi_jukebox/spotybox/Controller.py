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

    def stop_view(self):
        self._view.stop_view()
