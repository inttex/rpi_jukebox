import datetime
import warnings
import sys
import os
import pickle

import keyboard
import simpleaudio

LOCAL_DIRECTORY = os.path.join(os.path.dirname(__file__), 'local')
MUSICS_FILENAME = os.path.join(LOCAL_DIRECTORY, 'musics')
home = os.getenv('HOME')
# home = '/home/imam'
LOGFILE = os.path.join(home, '.log', 'jukebox')
MUSIC_DIRECTORY = os.path.join(home, 'Musique')

try:
    with open(MUSICS_FILENAME, 'rb') as myfile:
        musics = pickle.load(myfile)
except (EOFError, IOError):
    musics = dict()

def main():
    modify()

def run():
    play_obj = False
    while True:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=UserWarning)
            recorded = keyboard.record(until='enter')
        rfid = ''.join([el for el in keyboard.get_typed_strings(recorded)])
        now = datetime.datetime.now()
        msg = 'detected rfid no {} at {}\n'.format(rfid, now)
        with open(LOGFILE, 'a') as myfile:
            myfile.write(msg)
        if rfid in musics:
            music = musics[rfid]
            music_path = os.path.join(MUSIC_DIRECTORY, music)
            msg = 'play {}\n'.format(music)
            with open(LOGFILE, 'a') as myfile:
                myfile.write(msg)
            if play_obj:
                play_obj.stop()
            wave_obj = simpleaudio.WaveObject.from_wave_file(os.path.join(MUSIC_DIRECTORY, music))
            play_obj =wave_obj.play()

def modify():
    filenames = os.listdir(MUSIC_DIRECTORY)
    print('available musics')
    for index, filename in enumerate(filenames):
        print(index, filename, sep=': ')
    print('rfid to music correspondance:')
    print(musics)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', category=UserWarning)
        recorded = keyboard.record(until='enter')
    rfid = ''.join([el for el in keyboard.get_typed_strings(recorded)])
    print('I detected rfid number {}'.format(rfid))
    choice = input('to which music number do you want to associate it ({}-{}) (type q to quit or d to empty the table)?\n'.format(0,len(filenames)-1))
    if choice == 'q':
        sys.exit(0)
    if choice=='d':
        os.remove(MUSICS_FILENAME)
    else:
        try:
            index = int(choice)
            musics[rfid] = filenames[index]
        except (ValueError, IndexError):
            print('failed because of wrong number given!')
        else:
            with open(MUSICS_FILENAME, 'wb') as myfile:
                pickle.dump(musics, myfile)

if __name__=='__main__':
    main()
