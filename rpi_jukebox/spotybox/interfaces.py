from abc import ABC, abstractmethod

from rpi_jukebox.spotify_client.data_structs import Sp_Music


class ControllerInterface(ABC):

    @abstractmethod
    def evaluate_rfid(self, rfid_value: int):
        pass

    @abstractmethod
    def stop_view(self):
        pass

    @abstractmethod
    def pause_play(self):
        pass

    @abstractmethod
    def vol_inc(self):
        pass

    @abstractmethod
    def vol_dec(self):
        pass

    @abstractmethod
    def stop_device(self):
        pass

    @abstractmethod
    def stop_device_in_20min(self):
        pass

    @abstractmethod
    def next_track(self):
        pass

    @abstractmethod
    def prev_track(self):
        pass

    @abstractmethod
    def evaluate_new_switch_state(self, new_switch_state):
        pass


class ViewInterface(ABC):
    @abstractmethod
    def set_controller(self, controller: ControllerInterface):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def play_song(self, music: Sp_Music):
        pass

    @abstractmethod
    def stop_view(self):
        pass
