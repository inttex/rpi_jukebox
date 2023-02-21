from abc import ABC, abstractmethod

from rpi_jukebox.spotify_client.data_structs import Sp_Music, SwitchState


class ControllerInterface(ABC):

    @abstractmethod
    def evaluate_rfid(self, rfid_value: int):
        pass

    @abstractmethod
    def stop_view(self):
        pass

    @abstractmethod
    def evaluate_new_switch_state(self, new_switch_state:SwitchState):
        pass

    def stop_device(self):
        pass

    def stop_device_in_20min(self):
        pass


class ViewInterface(ABC):
    @abstractmethod
    def set_controller(self, controller: ControllerInterface):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop_view(self):
        pass
