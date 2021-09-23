import datetime
import warnings
import sys
import os
import requests

import keyboard
import simpleaudio

HOST = 'http://localhost:5000'

def main():
    resource = HOST + '/jukebox'
    rfid = 4
    rsp = requests.get(resource + '/{}'.format(rfid))
    status = rsp.status_code
    if status == 404:
        print('no resource, create a new one')
    elif status == 200:
        print('play music')
    else:
        print('no music, do nothing')

def run():
    play_obj = False
    while True:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=UserWarning)
            recorded = keyboard.record(until='enter')
        rfid = ''.join([el for el in keyboard.get_typed_strings(recorded)])
        now = datetime.datetime.now()
        msg = 'detected rfid no {} at {}\n'.format(rfid, now)
        print(msg)
        resource = HOST + '/jukebox'
        rsp = requests.get(resource + '/{}'.format(rfid))
        status = rsp.status_code
        if status == 404:
            create_new_resource(rfid)
        elif status == 200:
            play_obj = play_music(rsp, play_obj)
        else:
            print('no music, do nothing')

def create_new_resource(rfid):
    print('no resource, create a new one')

def play_music(rsp, play_obj):
    if play_obj:
        play_obj.stop()
    print('play music')
            # msg = 'play {}\n'.format(music)
            # print(msg)
    # wave_obj = simpleaudio.WaveObject.from_wave_file(os.path.join(MUSIC_DIRECTORY, music))
    # play_obj =wave_obj.play()
    return play_obj

if __name__=='__main__':
    main()
