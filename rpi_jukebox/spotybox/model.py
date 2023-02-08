import enum
import logging
from typing import Callable, NamedTuple

from rpi_jukebox.spotybox.interfaces import ControllerInterface


class COMMAND(enum.Enum):
    PAUSE_PLAY = enum.auto()
    VOL_INC = enum.auto()
    VOL_DEC = enum.auto()
    STOP_DEVICE = enum.auto()
    STOP_DEVICE_20_MIN = enum.auto()
    NEXT = enum.auto()
    PREV = enum.auto()
    STOP_VIEW = enum.auto()


class CommandID(NamedTuple):
    rdid: int
    command: COMMAND


RFID_NONE = -1


class Model:
    def __init__(self, ):
        # load cards from csv
        # read command_ids
        self._available_commands = {
            321939860424: COMMAND.PAUSE_PLAY,
            1077378640525: COMMAND.VOL_INC,
            321452272372: COMMAND.VOL_DEC,
            181471177607: COMMAND.STOP_DEVICE,
            937348065986: COMMAND.STOP_DEVICE_20_MIN,
            730221144919: COMMAND.NEXT,
            456312580711: COMMAND.PREV,
            700105795467: COMMAND.STOP_VIEW,  # elsa karte
        }

    def rfid_from_command(self, command_to_check: COMMAND):
        for key, command in self._available_commands.items():
            if command_to_check == command:
                print(command_to_check, key)
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

    def evaluate_rfid(self, rfid_value: int, callback: Callable, controller: ControllerInterface):
        logging.info('model: evaluating rfid %s' % rfid_value)

        if rfid_value in self._available_commands.keys():
            self.run_command(rfid_value, controller)
        else:
            callback(uri=111)
