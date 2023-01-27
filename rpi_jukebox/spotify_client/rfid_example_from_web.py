# see https://talaexe.com/moderndayrecordplayer
import configparser
from pathlib import Path

# !/usr/bin/env python

from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

config = configparser.ConfigParser()
configfile = Path(r'../../res/config.cfg')
config.read(configfile)
username = config['SPOTIFY']['username']
CLIENT_ID = config['SPOTIFY']['clientID']
CLIENT_SECRET = config['SPOTIFY']['clientSecret']
redirect_uri = config['SPOTIFY']['redirect_uri']
DEVICE_ID = config['SPOTIFY']['DEVICE_ID_VOLUMIO']

while True:
    try:
        reader = SimpleMFRC522()
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri=redirect_uri,
                                                       scope="user-read-playback-state,user-modify-playback-state"))

        # create an infinite while loop that will always be waiting for a new scan
        while True:
            print("Waiting for record scan...")
            id = reader.read()[0]
            print("Card Value is:", id)
            sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

            # DONT include the quotation marks around the card's ID value, just paste the number
            if (id == 'RFID-CARDVALUE-1'):

                # playing a song
                sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:2vSLxBSZoK0eha4AuhZlXV'])
                sleep(2)

            elif (id == 'RFID-CARDVALUE-2'):

                # playing an album
                sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:album:0JGOiO34nwfUdDrD612dOp')
                sleep(2)

            # continue adding as many "elifs" for songs/albums that you want to play

    # if there is an error, skip it and try the code again (i.e. timeout issues, no active device error, etc)
    except Exception as e:
        print(e)
        pass

    finally:
        print("Cleaning  up...")
        GPIO.cleanup()
