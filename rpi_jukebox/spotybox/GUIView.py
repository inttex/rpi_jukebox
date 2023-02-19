import logging
from rpi_jukebox.spotify_client.data_structs import Sp_Music
from rpi_jukebox.spotybox.csv_helper import get_commands
from rpi_jukebox.spotybox.dataclasses import COMMAND

from rpi_jukebox.spotybox.interfaces import ViewInterface, ControllerInterface
import dearpygui.dearpygui as dpg


class GUIView(ViewInterface):

    def __init__(self):
        pass

    def set_controller(self, controller: ControllerInterface):
        self._controller = controller

    def rfid_callback(self, _, __, rfid_value: tuple):
        self._controller.evaluate_rfid(rfid_value[0])

    def switch_callback(self, new_switch_state):
        self._controller.evaluate_new_switch_state(new_switch_state)

    def run(self):
        dpg.create_context()
        dpg.create_viewport(title='Custom Title', width=600, height=500)

        try:
            with dpg.window(label="Example Window"):
                dpg.add_text("Hello, world")
                dpg.add_button(label="Save")
                dpg.add_input_text(label="string", default_value="Quick brown fox")
                dpg.add_slider_float(label="float", default_value=0.273, max_value=1)
                available_commands = get_commands()
                for rfid, comm in available_commands.items():
                    comm: COMMAND
                    dpg.add_button(label=comm.name, user_data=(rfid,),
                                   callback=self.rfid_callback)
                # select RFID
                # toggle switcher
                # on off LED

            dpg.setup_dearpygui()
            dpg.show_viewport()
            dpg.start_dearpygui()


        finally:
            dpg.destroy_context()
            logging.info('rfid and reader threads are successfully joined')

    def stop_view(self):
        dpg.destroy_context()

    def play_song(self, music: Sp_Music):
        logging.info('view: playing song %s' % str(music))
        self._sp.start_playback(uris=[music.sp_uuid, ])
