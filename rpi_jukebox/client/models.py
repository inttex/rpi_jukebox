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
        self.rfid = None
        self.random_stop = None
        self.tmin = None
        self.tmax = None
        self.audio_segment = None
        self.start_stop_times = list()
        self.start_stop_index = 0

    def get_sound(self, wav_file):
        pass


if __name__=='__main__':
    main()
