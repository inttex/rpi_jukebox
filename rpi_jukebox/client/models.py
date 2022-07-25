def main():
    pass


class APICommunicator(object):

    """communicate by requests to the api restless server"""

    def __init__(self):
        """TODO: to be defined. """

    def get_music_file(self, rfid):
        """obtain wav file from server

        :rfid: TODO
        :returns: TODO

        """
        pass

    def get_random_stop(self):
        """TODO: Docstring for get_random_stop.

        :returns: TODO

        """
        pass

    def get_tmin(self):
        """TODO: Docstring for get_tmin.
        :returns: TODO

        """
        pass

    def get_tmax(self):
        """get max time for random_stop
        :returns: TODO

        """
        pass


class MusicLoader(object):

    """prepare the segment of music to be played"""

    def __init__(self):
        """TODO: to be defined. """
        self.rfid = None
        self.is_playing = False

    def get_sound(self, rfid, wav_file, random_stop=False, tmin=None, tmax=None):
        pass


if __name__=='__main__':
    main()
