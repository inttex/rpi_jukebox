import base64
import configparser
import sys
import urllib
from pathlib import Path

import requests
from spotipy import SpotifyOAuth, Spotify

import logging

logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.debug('This will get logged')

config = configparser.ConfigParser()

configfile = Path(r'../../res/config.cfg')
config.read(configfile)
username = config['SPOTIFY']['username']
clientID = config['SPOTIFY']['clientID']
clientSecret = config['SPOTIFY']['clientSecret']
redirect_uri = config['SPOTIFY']['redirect_uri']
DEVICE_ID = config['SPOTIFY']['DEVICE_ID_VOLUMIO']

sp = Spotify(auth_manager=SpotifyOAuth(username=username,
                                       client_id=DEVICE_ID,
                                       client_secret=clientSecret,
                                       redirect_uri=redirect_uri,
                                       scope="user-read-playback-state,user-modify-playback-state"))

sp.volume(80, device_id=DEVICE_ID)
# Transfer playback to the Raspberry Pi if music is playing on a different device
# sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

# Play the spotify track at URI with ID 45vW6Apg3QwawKzBi03rgD (you can swap this for a diff song ID below)
# sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:0bngtPi5C56c6IGB4h9XVS'])
# sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:4mHv2ujBeoqhwZxgVhoPJy'])  # the battle

sp.start_playback(uris=['spotify:track:4mHv2ujBeoqhwZxgVhoPJy'])  # the battle
# %%
asdf


def get_q_info():

    q = sp.queue()
    print('currently playing %s' % q['currently_playing']['name'])
    for i, track in enumerate(q['queue']):
        print('%i in queue: %s' % (i, track['name']))

def clear_queue():
    q = sp.queue()
    q_length = len(q['queue'])
    for i in range(q_length):
        sp.next_track()

'''
    playlist https://open.spotify.com/playlist/1kDpUGDtR0tb2eXob6ZrDD?si=815a94cec7604df1
    artist https://open.spotify.com/artist/0YC192cP3KPCRWx8zr8MfZ?si=9tGoyK36R2a1qkBo8GSV9w
    album https://open.spotify.com/album/6oU298pdPTCQnMx1PYwyUA?si=_k9JK4ccR4imkwXfkCVfeQ
    song https://open.spotify.com/track/6pWgRkpqVfxnj3WuIcJ7WP?si=e910db5eb272415f
    '''
context_url = 'https://open.spotify.com/playlist/3UqcGrPY6Jb7sloww3sH0X?si=2fe6ad1853ac4aab'
pl = sp.playlist('6GW1MH9yw8zA2AHDPW73cO')

pl = sp.playlist('3UqcGrPY6Jb7sloww3sH0X')
uris_in_pl = [track['track']['uri'] for track in pl['tracks']['items']]

sp.start_playback(context_uri=context_url, offset = {'uri':uris_in_pl[3]})


sp.start_playback(uris=[uris_in_pl[0], ])
[sp.add_to_queue(uri) for uri in uris_in_pl[1:4]]
sp.start_playback(uris=[uris_in_pl[3], ])

sp.add_to_queue(uris_in_pl[0])  # Wonderful Tonight
sp.add_to_queue(uris_in_pl[1])  # People Get Ready
sp.add_to_queue(uris_in_pl[2])  # Candle In The Wind - Remastered 2014
sp.add_to_queue(uris_in_pl[3])  # Against The Wind

sp.start_playback(uris=['spotify:track:3Rnwx4MD7Mm8JiFaIkmb5U', ]) #drei ??? serie 77 ep3
sp.track('3Rnwx4MD7Mm8JiFaIkmb5U')

sp.start_playback(uris = ['spotify:album:0VGqEmf8jbOIX0L5X8v8HD',])

# /connect-state/v1/player/command/from/595641fb2e820a76c55e92741481f09bcb19abe4/to/13dc7732c71e71ce9d3b3d7e38d67a748f0af9da

sp.add_to_queue()
q = sp.queue()
get_q_info()

clear_queue()

sp.pause_playback()
sp.start_playback()

sp.next_track()
sp.previous_track()

sp.current_user_playing_track()['is_playing']

# sp.start_playback(context_uri=['https://open.spotify.com/artist/4ogvuDRerGhZfSf7TtzHlr'])
# https://open.spotify.com/artist/4ogvuDRerGhZfSf7TtzHlr?si=kwtBuinBS6qGOplooSbfAg
# sp.start_playback(device_id=DEVICE_ID,uris=['spotify:artist:0TnOYISbd1XYRBk9myaseg'])
# sp.start_playback(uris=['spotify:artist:3jOstUTkEu2JkjvRdBA5Gu',]) # only works for album...

# the following are working
sp.start_playback(context_uri='https://open.spotify.com/album/6oU298pdPTCQnMx1PYwyUA')  # only works for album...
sp.start_playback(context_uri='https://open.spotify.com/album/5XgEM5g3xWEwL4Zr6UjoLo')

sp.start_playback(uris=['spotify:track:3oQomOPRNQ5NVFUmLJHbAV'])

urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'
artist = sp.artist(urn)
print(artist)

album = sp.album('6oU298pdPTCQnMx1PYwyUA')
print(album)

# https://open.spotify.com/track/6ZFbXIJkuI1dVNWvzJzown?si=2fcfd03b293145c8
asdf
# %%

elsa_album = 'https://open.spotify.com/album/5KZIfY66uP6N0WvZ1k7YJC?si=owUejvEtSO6_GFrTI5C6bg'
elsa_uri = elsa_album \
    .replace('https://open.spotify.com/', 'spotify:') \
    .replace('album/', 'album:').split('?si')[0]

res = sp.album(elsa_uri)
img_url = res['images'][0]['url']

# img_data = requests.get(img_url).content
# with open('image_name.jpg', 'wb') as handler:
#     print(handler.write(img_data))
urllib.request.urlretrieve(img_url, "my_spotify_img.jpg")

# decodeit = open('hello_level.jpeg', 'wb')
# decodeit.write(base64.b64decode((img_data)))
# decodeit.close()

# %%


# get current song in album
info_dict = sp.currently_playing(market='CH', additional_types=None)
info_dict = sp.currently_playing()['item']['external_urls']['spotify']

album_uri = info_dict['item']['album']['id']
song_uri = info_dict['item']['id']
progress_ms = info_dict['progress_ms']

# start_playback(device_id=None, context_uri=None, uris=None, offset=None, position_ms=progress_ms)
sp.start_playback(uris=[f'spotify:track:{song_uri}'], position_ms=progress_ms)

sp.volume(100, device_id=None)

sp.devices()
