import logging
from typing import Callable, NamedTuple

from rpi_jukebox.spotify_client.data_structs import Sp_Music, SpType, ReplayType
from rpi_jukebox.spotybox.csv_helper import get_commands, get_collection
from rpi_jukebox.spotybox.dataclasses import COMMAND

from rpi_jukebox.spotybox.interfaces import ControllerInterface


class CommandID(NamedTuple):
    rdid: int
    command: COMMAND


RFID_NONE = -1


class Collection:
    def __init__(self):
        # read albums from csv
        # read playlists from csv
        pass


class Model:
    def __init__(self, ):
        self._available_commands = get_commands()
        self._my_collection = get_collection()
        self._collection = Collection()

    def rfid_from_command(self, command_to_check: COMMAND):
        for key, command in self._available_commands.items():
            if command_to_check == command:
                return key
        return RFID_NONE

    def run_command(self, rfid_value, controller: ControllerInterface):
        if rfid_value == self.rfid_from_command(COMMAND.STOP_VIEW):
            controller.stop_view()
        elif rfid_value == self.rfid_from_command(COMMAND.PAUSE_PLAY):
            controller.pause_play()
        elif rfid_value == self.rfid_from_command(COMMAND.VOL_INC):
            controller.vol_inc()
        elif rfid_value == self.rfid_from_command(COMMAND.VOL_DEC):
            controller.vol_dec()
        elif rfid_value == self.rfid_from_command(COMMAND.STOP_DEVICE):
            controller.stop_device()
        elif rfid_value == self.rfid_from_command(COMMAND.STOP_DEVICE_20_MIN):
            controller.stop_device_in_20min()
        elif rfid_value == self.rfid_from_command(COMMAND.NEXT):
            controller.next_track()
        elif rfid_value == self.rfid_from_command(COMMAND.PREV):
            controller.prev_track()
        else:
            logging.info('command for rfid %s not found' % rfid_value)

    def evaluate_rfid(self, rfid_value: int, controller: ControllerInterface):
        logging.info('model: evaluating rfid %s' % rfid_value)

        if rfid_value in self._available_commands.keys():
            self.run_command(rfid_value, controller)
        elif rfid_value in self._my_collection.keys():
            controller.play_entry(self._my_collection[rfid_value])
        # elif rfid_value == 700105795467:  # elsa karte
        #     music = Sp_Music(rfid=700105795467,
        #                      title='testPL', sp_uuid='3UqcGrPY6Jb7sloww3sH0X',
        #                      sp_type=SpType.PLAYLIST, replay_type=ReplayType.FROM_START,
        #                      last_played_song=0)
        #     controller.play_entry(music)  # testPL
        else:
            logging.info('rfid %s not found' % rfid_value)
