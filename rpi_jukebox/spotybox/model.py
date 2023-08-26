import configparser
import logging
import os
import traceback
from pathlib import Path
from threading import Thread, Lock
from time import sleep
from typing import NamedTuple, Callable

from spotipy import SpotifyOAuth, Spotify, SpotifyOauthError

from rpi_jukebox.spotify_client.data_structs import Sp_Music, SpType, get_uri_from_url, ReplayType, SwitchState, Device
from rpi_jukebox.spotybox.csv_helper import get_commands, get_collection, write_collection
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


class SpPlayer:
    def __init__(self, update_collection: Callable):
        self._currently_playing_music: Sp_Music = None
        self._volume = 40
        self._sp = self.start_spotify_connection()
        self._do_stop_threads = False
        self._lock = Lock()
        self._current_track_getter_thread = Thread(target=self.current_track_getter_loop,
                                                   args=(lambda: self._do_stop_threads, self._lock))
        self._current_track_getter_thread.start()
        self._update_collection: Callable = update_collection

    def __del__(self):
        self._do_stop_threads = True
        self._current_track_getter_thread.join()
        logging.info('track getter thread terminated by flag in destructor')

    def current_track_getter_loop(self, is_do_stop_threads: Callable, lock: Lock):
        while not is_do_stop_threads():
            for i in range(3):
                sleep(1)
                if is_do_stop_threads():
                    break
            try:
                with lock:
                    current_track = self._sp.currently_playing()['item']['external_urls']['spotify']
                    if (self._currently_playing_music is not None) and (
                            self._currently_playing_music.replay_type == ReplayType.FROM_LAST_TRACK) and (
                            current_track != self._currently_playing_music.last_played_song):
                        logging.info('current track has changed to %s' % current_track)
                        self._currently_playing_music = self._currently_playing_music._replace(
                            last_played_song=current_track)
                        self._update_collection(self._currently_playing_music)
            except:
                print('current track getter loop: %s' % traceback.print_exc())

    def start_spotify_connection(self):
        config = configparser.ConfigParser()
        configfile = Path(r'../../res/config.cfg')
        config.read(configfile)
        username = config['SPOTIFY']['username']
        self.clientID = config['SPOTIFY']['clientID']
        clientSecret = config['SPOTIFY']['clientSecret']
        redirect_uri = config['SPOTIFY']['redirect_uri']
        self._device_id_internal = Device('internal', config['SPOTIFY']['DEVICE_ID_VOLUMIO'])
        self._device_id_external = Device('external', config['SPOTIFY']['DEVICE_ID_LINUX'])
        self._device = self._device_id_internal

        sp = Spotify(auth_manager=SpotifyOAuth(username=username,
                                               client_id=self.clientID,
                                               client_secret=clientSecret,
                                               redirect_uri=redirect_uri,
                                               scope="user-read-playback-state,user-modify-playback-state",
                                               open_browser=False))

        sp.volume(self._volume, device_id=self._device.device_id)
        return sp

    def play_entry(self, music: Sp_Music):
        try:
            with self._lock:
                self._currently_playing_music = music
                logging.info(
                    'Sp_Player: playing album/playlist "%s" with id %s of type %s, track %s on device %s' % (
                        str(music.title), str(music), music.sp_type, str(music.last_played_song), str(self._device.name)))
                if music.sp_type == SpType.ALBUM:
                    self._sp.start_playback(device_id=self._device.device_id, context_uri=music.sp_link)
                elif music.sp_type == SpType.PLAYLIST:
                    print('play', music.last_played_song)
                    if music.replay_type == ReplayType.FROM_LAST_TRACK:
                        self._sp.start_playback(device_id=self._device.device_id,
                                                context_uri=music.sp_link,
                                                offset={'uri': get_uri_from_url(music.last_played_song)})
                    elif music.replay_type == ReplayType.FROM_START:
                        self._sp.start_playback(device_id=self._device.device_id,
                                                context_uri=music.sp_link)
        except SpotifyOauthError:
            logging.exception('sp_player play_entry: %s', traceback.print_exc())

    def pause_play(self):
        if self._sp.current_user_playing_track()['is_playing']:
            logging.info('Sp_Player: toggling to PAUSING')
            self._sp.pause_playback()
        else:
            logging.info('Sp_Player: toggling to PLAYING')
            self._sp.start_playback()

    def prev_track(self):
        logging.info('Sp_Player: prev track')
        self._sp.previous_track()

    def next_track(self):
        logging.info('Sp_Player: next track')
        self._sp.next_track()

    def vol_dec(self):
        self._volume -= 10
        self._volume = max([0, min([self._volume, 100])])
        logging.info('Sp_Player: decrease volume to %s' % self._volume)
        self._sp.volume(self._volume)

    def vol_inc(self):
        self._volume += 10
        self._volume = max([0, min([self._volume, 100])])
        logging.info('Sp_Player: increase volume to %s' % self._volume)
        self._sp.volume(self._volume)

    def stop_device_in_20min(self):
        logging.info('Sp_Player: stop in 20min. NOT IMPLEMENTED, YET')
        # logging.info('Sp_Player: do stop raspi now, instead')
        # os.system('shutdown -h now')

    def set_switch_state(self, new_switch_state: SwitchState):
        if new_switch_state == SwitchState.INTERNAL:
            self._device = self._device_id_internal
        else:
            self._device = self._device_id_external
        logging.info('switch to replay device %s' % self._device.name)
        self._sp.transfer_playback(device_id=self._device.device_id)


class Model:
    def __init__(self, ):
        self._available_commands = get_commands()
        self._my_collection = get_collection()
        self._collection = Collection()
        for i in range(100):
            try:
                sleep(1)
                logging.info('trying to start SpPlayer, nb %s' % i)
                self._sp_player = SpPlayer(self.update_collection)
                logging.info('successful try, nb %s' % i)
                break
            except:
                logging.info('failed try, nb %s' % i)
                logging.info(traceback.print_exc())

    def update_collection(self, updated_music_entry: Sp_Music):
        logging.info('updating collection')
        self._my_collection.update({updated_music_entry.rfid: updated_music_entry})
        write_collection(self._my_collection)

    def rfid_from_command(self, command_to_check: COMMAND):
        for key, command in self._available_commands.items():
            if command_to_check == command:
                return key
        return RFID_NONE

    def run_command(self, rfid_value, controller: ControllerInterface):
        if rfid_value == self.rfid_from_command(COMMAND.STOP_VIEW):
            controller.stop_view()
        elif rfid_value == self.rfid_from_command(COMMAND.PAUSE_PLAY):
            self._sp_player.pause_play()
        elif rfid_value == self.rfid_from_command(COMMAND.VOL_INC):
            self._sp_player.vol_inc()
        elif rfid_value == self.rfid_from_command(COMMAND.VOL_DEC):
            self._sp_player.vol_dec()
        elif rfid_value == self.rfid_from_command(COMMAND.STOP_DEVICE):
            controller.stop_device()
        elif rfid_value == self.rfid_from_command(COMMAND.STOP_DEVICE_20_MIN):
            self._sp_player.stop_device_in_20min()
        elif rfid_value == self.rfid_from_command(COMMAND.NEXT):
            self._sp_player.next_track()
        elif rfid_value == self.rfid_from_command(COMMAND.PREV):
            self._sp_player.prev_track()
        else:
            logging.info('command for rfid %s not found' % rfid_value)

    def evaluate_rfid(self, rfid_value: int, controller: ControllerInterface):
        logging.info('model: evaluating rfid %s' % rfid_value)

        if rfid_value in self._available_commands.keys():
            self.run_command(rfid_value, controller)
        elif rfid_value in self._my_collection.keys():
            self._sp_player.play_entry(self._my_collection[rfid_value])
        else:
            logging.info('rfid %s not found' % rfid_value)

    def stop_model(self):
        self._sp_player.__del__()

    def set_switch_state(self, new_switch_state: SwitchState):
        self._sp_player.set_switch_state(new_switch_state)
