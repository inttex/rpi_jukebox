import configparser
from pathlib import Path

from spotipy import SpotifyOAuth, Spotify

config = configparser.ConfigParser()

configfile = Path(r'../../res/config.cfg')
config.read(configfile)
username = config['SPOTIFY']['username']
clientID = config['SPOTIFY']['clientID']
clientSecret = config['SPOTIFY']['clientSecret']
redirect_uri = config['SPOTIFY']['redirect_uri']
DEVICE_ID = config['SPOTIFY']['DEVICE_ID_VOLUMIO']

sp = Spotify(auth_manager=SpotifyOAuth(username=username,
                                       client_id=clientID,
                                       client_secret=clientSecret,
                                       redirect_uri=redirect_uri,
                                       scope="user-read-playback-state,user-modify-playback-state"))
# Transfer playback to the Raspberry Pi if music is playing on a different device
sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

# Play the spotify track at URI with ID 45vW6Apg3QwawKzBi03rgD (you can swap this for a diff song ID below)
# sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:0bngtPi5C56c6IGB4h9XVS'])
sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:4mHv2ujBeoqhwZxgVhoPJy'])  # the battle

# %%

# get current song in album
info_dict = sp.currently_playing(market='CH', additional_types=None)

album_uri = info_dict['item']['album']['id']
song_uri = info_dict['item']['id']
progress_ms = info_dict['progress_ms']

# start_playback(device_id=None, context_uri=None, uris=None, offset=None, position_ms=progress_ms)
sp.start_playback(uris=[f'spotify:track:{song_uri}'], position_ms=progress_ms)

sp.volume(100, device_id=None)

sp.devices()
