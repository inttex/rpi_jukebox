import datetime
import warnings
import sys
import os

import keyboard
import simpleaudio

def main():
    run()

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
            # msg = 'play {}\n'.format(music)
            # print(msg)
        if play_obj:
            play_obj.stop()
        # wave_obj = simpleaudio.WaveObject.from_wave_file(os.path.join(MUSIC_DIRECTORY, music))
        # play_obj =wave_obj.play()

if __name__=='__main__':
    main()
