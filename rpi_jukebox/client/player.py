import datetime
import warnings
import sys
import os
import threading
import random

import requests
import keyboard
import simpleaudio

HOST = 'http://localhost:5000'
TMIN = 5
TMAX = 20

def main():
    run()
    # run()
    # resource = HOST + '/jukebox'
    # rfid = 1
    # rsp = requests.get(resource + '/{}'.format(rfid))
    # status = rsp.status_code
    # print(status)
    # # create_new_resource(rfid)
    # play_obj = play_music(rsp, False)
    # play_obj.wait_done()


def run():
    play_obj = False
    previous_rfid = None
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
            if not rfid==previous_rfid:
                simpleaudio.stop_all()
                play_obj = play_music(rsp)
            else:
                if play_obj.is_playing():
                    play_obj.pause()
                    play_obj.resume()
                else:
                    play_obj = play_music(rsp)
            url = HOST + '/parameters/random_stop'
            rsp = requests.get(url)
            random_stop = rsp.json()
            if random_stop:
                time = random.randint(TMIN, TMAX)
                random_stopper = threading.Timer(time, play_obj.pause)
                random_stopper.start()
            previous_rfid = rfid
        else:
            print('no music, do nothing')

def create_new_resource(rfid):
    resource = HOST + '/jukebox'
    rsp = requests.post(resource, data={'rfid': rfid})

def play_music(rsp):
    binary = rsp.content
    with open('temp.wav', 'wb') as myfile:
        myfile.write(binary)
    wave_obj = simpleaudio.WaveObject.from_wave_file('temp.wav')
    play_obj = wave_obj.play()
    os.remove('temp.wav')
    return play_obj

if __name__=='__main__':
    main()
