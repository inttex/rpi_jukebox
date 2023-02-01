import enum
import logging
from typing import Callable, NamedTuple

from rpi_jukebox.spotybox.interfaces import ControllerInterface


class COMMAND(enum.Enum):
    PAUSE_PLAY = enum.auto
    VOL_INC = enum.auto
    VOL_DEC = enum.auto
    STOP_DEVICE = enum.auto
    STOP_DEVICE_20_MIN = enum.auto
    NEXT = enum.auto
    PREV = enum.auto
    STOP_VIEW = enum.auto


class CommandID(NamedTuple):
    rdid: int
    command: COMMAND


class Model:
    def __init__(self, ):
        # load cards from csv
        # read command_ids
        self._available_commands = {
            1231251235: COMMAND.PAUSE_PLAY,
            4545080823: COMMAND.VOL_INC,
            3244684523: COMMAND.VOL_DEC,
            # 3244684523 : COMMAND.STOP_DEVICE,
            # 3244684523 : COMMAND.STOP_DEVICE_20_MIN,
            # 3244684523 : COMMAND.NEXT,
            700105795467: COMMAND.STOP_VIEW,
        }

    def evaluate_rfid(self, rfid_value: int, callback: Callable, controller: ControllerInterface):
        logging.info('model: evaluating rfid %s' % rfid_value)

        # if rfid_value in self._available_commands.keys():
        #     if rfid_value ==
        if rfid_value == 700105795467: #COMMAND.STOP_VIEW,
            controller.stop_view()
        else:
            callback(uri=111)
