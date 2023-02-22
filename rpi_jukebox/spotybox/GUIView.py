import enum
import logging
from enum import Enum

import dearpygui.dearpygui as dpg

from rpi_jukebox.spotify_client.data_structs import Sp_Music, SwitchState
from rpi_jukebox.spotybox.csv_helper import get_commands, get_collection
from rpi_jukebox.spotybox.dataclasses import COMMAND
from rpi_jukebox.spotybox.interfaces import ViewInterface, ControllerInterface


class PLAY_STATUS(Enum):
    PLAYING = enum.auto()
    PAUSING = enum.auto()


class GUIView(ViewInterface):

    def __init__(self):
        pass

    def set_controller(self, controller: ControllerInterface):
        self._controller = controller

    def rfid_callback(self, _, __, rfid_value: tuple):
        self._controller.evaluate_rfid(rfid_value[0])

    def switch_callback(self):
        new_switch_state = SwitchState[dpg.get_value('renderer_switch')]
        logging.info('switch callback %s' % dpg.get_value('renderer_switch'))
        self._controller.evaluate_new_switch_state(new_switch_state)

    def run(self):
        dpg.create_context()
        dpg.create_viewport(title='Custom Title', width=900, height=500)

        try:
            with dpg.window(label="Example Window"):
                with dpg.group(horizontal=True):
                    with dpg.child_window(width=250, height=450):
                        dpg.add_text("Physical I/O")
                        dpg.add_separator()
                        dpg.add_text("Renderer:")
                        dpg.add_radio_button(tag='renderer_switch', items=(SwitchState.INTERNAL.name,
                                                                           SwitchState.EXTERNAL.name),
                                             callback=self.switch_callback)
                        dpg.add_text("LED:")
                        dpg.add_color_button(label='LED', default_value=(0, 255, 0))
                    with dpg.child_window(label='Commands', width=250):
                        dpg.add_text("RFID Commands")
                        dpg.add_separator()
                        available_commands = get_commands()
                        for rfid, comm in available_commands.items():
                            comm: COMMAND
                            dpg.add_button(label=comm.name, user_data=(rfid,),
                                           callback=self.rfid_callback)

                    with dpg.child_window(label='My Collection', width=250):
                        dpg.add_text("RFID Collection Cards")
                        dpg.add_separator()
                        for rfid, entry in get_collection().items():
                            # print(entry)
                            entry: Sp_Music
                            dpg.add_button(label=entry.title, user_data=(rfid,),
                                           callback=self.rfid_callback)

            dpg.setup_dearpygui()
            dpg.show_viewport()
            dpg.start_dearpygui()


        finally:
            dpg.destroy_context()
            self._controller.stop_view()

    def stop_view(self):
        dpg.destroy_context()
