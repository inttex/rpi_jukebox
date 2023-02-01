from abc import ABC, abstractmethod


class ControllerInterface(ABC):

    @abstractmethod
    def evaluate_rfid(self, rfid_value: int):
        pass

    @abstractmethod
    def stop_view(self):
        pass


class ViewInterface(ABC):
    @abstractmethod
    def set_controller(self, controller: ControllerInterface):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def play_song(self, uri):
        pass

    @abstractmethod
    def stop_view(self):
        pass
