import enum
from typing import NamedTuple, List


class SpType(enum.Enum):
    ALBUM = 1
    PLAYLIST = 2


class ReplayType(enum.Enum):
    FROM_START = 1
    FROM_LAST_TRACK = 2


class SwitchState(enum.Enum):
    INTERNAL = 1
    EXTERNAL = 2


def get_uri_from_url(url):
    uri = url.replace('https://open.spotify.com/', 'spotify:')
    if 'album' in uri:
        uri = uri.replace('album/', 'album:')
    elif 'playlist' in uri:
        uri = uri.replace('playlist/', 'playlist:')
    elif 'artist' in uri:
        uri = uri.replace('artist/', 'artist:')
    elif 'track' in uri:
        uri = uri.replace('track/', 'track:')
    uri = uri.split('?si')[0]
    return uri


def get_uuid_from_url(url):
    uri = get_uri_from_url(url)
    uuid = uri.split(':')[2]
    return uuid


class CardLabel(NamedTuple):
    name: str
    url: str
    label_for_print: str = ''
    img = None

    def get_uuid(self):
        return get_uuid_from_url(self.url)

    def get_uri(self):
        return get_uri_from_url(self.url)


class Sp_Music(NamedTuple):
    rfid: int = 0
    title: str = 'new title'
    sp_link: str = 'asdf'
    sp_type: SpType = SpType.ALBUM
    replay_type: ReplayType = ReplayType.FROM_START
    last_played_song: str = ''

    def __repr__(self):
        return self.get_sp_uuid()

    def __str__(self):
        return self.__repr__()

    def get_sp_uri(self):
        return get_uri_from_url(self.sp_link)

    def get_sp_uuid(self):
        return get_uuid_from_url(self.sp_link)


class Sp_Card(NamedTuple):
    rfid: int
    card_label: CardLabel
    music: Sp_Music
