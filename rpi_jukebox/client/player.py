import datetime
import warnings
import os
import threading
import random
import logging

import requests
import simpleaudio

from rpi_jukebox.api.config import CLIENT_LOG_FILE

HOST = 'http://localhost:43210'
TMIN = 5
TMAX = 20

logging.basicConfig(filename=CLIENT_LOG_FILE, level=logging.DEBUG, format='%(asctime)s %(message)s')

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
            logging.info('wait for next keyboard input...')
            if play_obj:
                logging.debug('the play object id is %s', play_obj.play_id)
            recorded = keyboard.record(until='enter')
        rfid = ''.join([el for el in keyboard.get_typed_strings(recorded)])
        now = datetime.datetime.now()
        logging.info('detected rfid no %s', rfid)
        resource = HOST + '/jukebox'
        rsp = requests.get(resource + '/{}'.format(rfid))
        status = rsp.status_code
        if status == 404:
            create_new_resource(rfid)
            logging.info('create new entry point for this rfid')
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
                TIME = random.randint(TMIN, TMAX)
                random_stopper = threading.Timer(TIME, play_obj.pause)
                logging.info('the music of play object no %s will be paused in %s s', play_obj.play_id, TIME)
                random_stopper.start()
            previous_rfid = rfid
        else:
            logging.info('did not get a music, do nothing')

def create_new_resource(rfid):
    resource = HOST + '/jukebox'
    rsp = requests.post(resource, data={'rfid': rfid})

def play_music(rsp):
    binary = rsp.content
    with open('temp.wav', 'wb') as myfile:
        myfile.write(binary)
    wave_obj = simpleaudio.WaveObject.from_wave_file('temp.wav')
    play_obj = wave_obj.play()
    logging.info('start playing play object no %s ...', play_obj.play_id)
    os.remove('temp.wav')
    return play_obj

if __name__=='__main__':
    main()
