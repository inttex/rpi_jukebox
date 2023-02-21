import configparser
import enum
import logging
from enum import Enum
from pathlib import Path

from spotipy import Spotify, SpotifyOAuth

from rpi_jukebox.spotify_client.data_structs import Sp_Music, SpType
from rpi_jukebox.spotybox.csv_helper import get_commands, get_collection
from rpi_jukebox.spotybox.dataclasses import COMMAND

from rpi_jukebox.spotybox.interfaces import ViewInterface, ControllerInterface
import dearpygui.dearpygui as dpg


class PLAY_STATUS(Enum):
    PLAYING = enum.auto()
    PAUSING = enum.auto()


class GUIView(ViewInterface):

    def __init__(self):
        self._volume = 80
        self._sp = self.start_spotify_connection()


    def set_controller(self, controller: ControllerInterface):
        self._controller = controller

    def start_spotify_connection(self):
        config = configparser.ConfigParser()
        configfile = Path(r'../../res/config.cfg')
        config.read(configfile)
        username = config['SPOTIFY']['username']
        clientID = config['SPOTIFY']['clientID']
        clientSecret = config['SPOTIFY']['clientSecret']
        redirect_uri = config['SPOTIFY']['redirect_uri']
        self._DEVICE_ID = config['SPOTIFY']['DEVICE_ID_LINUX']

        sp = Spotify(auth_manager=SpotifyOAuth(username=username,
                                               client_id=clientID,
                                               client_secret=clientSecret,
                                               redirect_uri=redirect_uri,
                                               scope="user-read-playback-state,user-modify-playback-state",
                                               open_browser=False))

        sp.volume(self._volume)
        return sp

    def rfid_callback(self, _, __, rfid_value: tuple):
        self._controller.evaluate_rfid(rfid_value[0])

    def switch_callback(self, new_switch_state):
        self._controller.evaluate_new_switch_state(new_switch_state)

    def run(self):
        dpg.create_context()
        dpg.create_viewport(title='Custom Title', width=900, height=500)

        try:
            with dpg.window(label="Example Window"):
                with dpg.group(horizontal=True):
                    with dpg.child_window(width = 250, height = 450):
                        dpg.add_text("Physical I/O")
                        dpg.add_separator()
                        dpg.add_text("Renderer:")
                        dpg.add_radio_button(label = 'Renderer', items=('local','external'))
                        dpg.add_text("LED:")
                        dpg.add_color_button(label = 'LED',default_value=(0,255,0))
                    with dpg.child_window(label = 'Commands',width = 250):
                        dpg.add_text("RFID Commands")
                        dpg.add_separator()
                        available_commands = get_commands()
                        for rfid, comm in available_commands.items():
                            comm: COMMAND
                            dpg.add_button(label=comm.name, user_data=(rfid,),
                                       callback=self.rfid_callback)

                    with dpg.child_window(label = 'My Collection',width = 250):
                        dpg.add_text("RFID Collection Cards")
                        dpg.add_separator()
                        for rfid, entry in get_collection().items():
                            print(entry)
                            entry: Sp_Music
                            dpg.add_button(label=entry.title, user_data=(rfid,),
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

    def _clear_queue(self):
        q = self._sp.queue()
        q_length = len(q['queue'])
        for i in range(q_length):
            self._sp.next_track()

    def play_song(self, music: Sp_Music):
        logging.info('view: playing song %s' % str(music))
        # self._clear_queue()
        if music.sp_type == SpType.ALBUM:
            self._sp.start_playback(context_uri=music.sp_link)
        if music.sp_type == SpType.PLAYLIST:
            self._sp.start_playback(context_uri=music.sp_link, offset={'position': music.last_played_song})

    def pause_play(self):
        if self._sp.current_user_playing_track()['is_playing']:
            logging.info('GUI_View: toggling to PAUSING')
            self._sp.pause_playback()
        else:
            logging.info('GUI_View: toggling to PLAYING')
            self._sp.start_playback()

    def prev_track(self):
        logging.info('GUI_View: prev track')
        self._sp.previous_track()

    def next_track(self):
        logging.info('GUI_View: next track')
        self._sp.next_track()

    def vol_dec(self):
        self._volume -= 10
        self._volume = max([0, min([self._volume, 100])])
        logging.info('GUI_View: decrease volume to %s'%self._volume)
        self._sp.volume(self._volume)

    def vol_inc(self):
        self._volume += 10
        self._volume = max([0, min([self._volume, 100])])
        logging.info('GUI_View: increase volume to %s' % self._volume)
        self._sp.volume(self._volume)

    def stop_view_in20min(self):
        logging.info('GUI_View: stop in 20min. NOT IMPLEMENTED, YET')
