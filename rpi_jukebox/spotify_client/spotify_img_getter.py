import configparser
import csv
import urllib
from pathlib import Path

from spotipy import SpotifyOAuth, Spotify

import logging

# logging.basicConfig(level=logging.DEBUG)
# logging.debug('This will get logged')

config = configparser.ConfigParser()

configfile = Path(r'../../res/config.cfg')
config.read(configfile)
username = config['SPOTIFY']['username']
clientID = config['SPOTIFY']['clientID']
clientSecret = config['SPOTIFY']['clientSecret']
redirect_uri = config['SPOTIFY']['redirect_uri']
DEVICE_ID = config['SPOTIFY']['DEVICE_ID_LINUX']


def get_img_for_album(sp: Spotify, uri, uuid, img_folder: Path):
    album_infos = sp.album(uri)
    img_url = album_infos['images'][0]['url']  # get the image with the highes resolution
    urllib.request.urlretrieve(img_url, img_folder.joinpath("img_%s.jpg" % uuid))


def create_uri_n_uuid_for_album(album_url):
    uri = album_url \
        .replace('https://open.spotify.com/', 'spotify:') \
        .replace('album/', 'album:').split('?si')[0]
    uuid = uri.split(':')[2]
    return uri, uuid


def main():
    img_folder = Path(r'imgs')

    sp = Spotify(auth_manager=SpotifyOAuth(username=username,
                                           client_id=clientID,
                                           client_secret=clientSecret,
                                           redirect_uri=redirect_uri,
                                           scope="user-read-playback-state,user-modify-playback-state"))

    with open('albums_to_get.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        albums = [row for row in spamreader]

    for title, url in albums:
        print('getting image for album with title:',title)
        uri, uuid = create_uri_n_uuid_for_album(url)
        get_img_for_album(sp, uri, uuid, img_folder)


if __name__ == '__main__':
    main()
