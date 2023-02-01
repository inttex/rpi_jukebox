import enum
from typing import NamedTuple, List


class SpType(enum.Enum):
    ALBUM = enum.auto
    PLAYLIST = enum.auto


class ReplayType(enum.Enum):
    FROM_START = 1
    FROM_LAST_TRACK = 2


class CardLabel(NamedTuple):
    name: str
    url: str
    label_for_print: str = ''
    img = None

    def get_uri(self):
        uri = self.url.replace('https://open.spotify.com/', 'spotify:')
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

    def get_uuid(self):
        uri = self.get_uri()
        uuid = uri.split(':')[2]
        return uuid


class Sp_Music(NamedTuple):
    id: int = 0
    rfid: int = 0
    title: str = 'new title'
    sp_uuid: str = 'asdf'
    sp_type: SpType = SpType.ALBUM
    replay_type: ReplayType = ReplayType.FROM_START
    last_played_song: str = 0


class Sp_Card(NamedTuple):
    rfid: int
    card_label: CardLabel
    music: Sp_Music
