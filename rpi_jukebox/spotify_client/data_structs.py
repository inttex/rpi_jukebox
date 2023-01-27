import enum
from typing import NamedTuple, List


class SpType(enum.Enum):
    SONG = 1
    ALBUM = 2
    PLAYLIST = 4
    PLAYLIST_RANDOM_ALBUM = 5
    ARTIST_RANDOM_ALBUM = 6


class ReplayType(enum.Enum):
    FROM_START = 1
    FROM_LAST_TRACK = 2
    FROM_RANDOM_TRACK = 3


class Spotify_URL:
    '''
    playlist https://open.spotify.com/playlist/1kDpUGDtR0tb2eXob6ZrDD?si=815a94cec7604df1
    artist https://open.spotify.com/artist/0YC192cP3KPCRWx8zr8MfZ?si=9tGoyK36R2a1qkBo8GSV9w
    album https://open.spotify.com/album/6oU298pdPTCQnMx1PYwyUA?si=_k9JK4ccR4imkwXfkCVfeQ
    song https://open.spotify.com/track/6pWgRkpqVfxnj3WuIcJ7WP?si=e910db5eb272415f
    '''

    def __int__(self, full_url_string:str):
        splits = full_url_string.split(r'/')
        type, uuid  = splits[3], splits[4]


class Sp_Musics(NamedTuple):
    id: int = 0
    rfid: int = 0
    title: str = 'new title'
    sp_uuid: str = 'asdf'
    sp_type: SpType = SpType.SONG
    replay_type: ReplayType = ReplayType.FROM_START
    image: List[int] = []
    last_played_album: str = 0
    last_played_song: str = 0
    last_timestamp_ms: int = 0


def main():
    music = Sp_Musics(1, 1234, 'the battle', 'spotify:track:4mHv2ujBeoqhwZxgVhoPJy',
                      SpType.SONG, ReplayType.FROM_START)


if __name__ == '__main__':
    main()
