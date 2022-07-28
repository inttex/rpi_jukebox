import requests


def main():
    HOST = 'http://localhost:5000'
    api_communicator = APICommunicator(HOST)
    api_communicator2 = APICommunicator('abc')
    print(api_communicator.url)
    print(api_communicator2.url)
    # rfid = 1
    # wav_file, success = api_communicator.get_music_file(rfid)
    # print(wav_file)
    # print(success)


class APICommunicator(object):

    """communicate by requests to the api restless server"""
    entry_points = dict(
            jukebox='/jukebox',
            random_stop='/parameters/random_stop',
            tmin='parameters/tmin',
            tmax='parameters/tmax',
            )

    def __init__(self, host):
        """TODO: to be defined. """
        self.host = host
        self.url ={name: self.host + '/' + entry for name, entry in self.entry_points.items()}

    def get_music_file(self, rfid):
        """obtain wav file from server

        :rfid: TODO
        :returns: wav_file, success

        """
        url = f'{self.url['jukebox']}/{rfid}'

        # rsp = requests.get(url)
        # status = rsp.status_code
        # if status == 404:
            # create_new_resource(rfid)
            # logging.info('create new entry point for this rfid')
        # elif status == 200:
            # if not rfid==previous_rfid:
                # simpleaudio.stop_all()
                # play_obj = play_music(rsp)
            # else:
                # if play_obj.is_playing():
                    # play_obj.pause()
                    # play_obj.resume()
                # else:
                    # play_obj = play_music(rsp)
            # url = HOST + '/parameters/random_stop'
            # rsp = requests.get(url)
            # random_stop = rsp.json()
            # if random_stop:
                # TIME = random.randint(TMIN, TMAX)
                # random_stopper = threading.Timer(TIME, play_obj.pause)
                # logging.info('the music of play object no %s will be paused in %s s', play_obj.play_id, TIME)
                # random_stopper.start()
            # previous_rfid = rfid
        # else:
            # logging.info('did not get a music, do nothing')

        wav_file = None
        return wav_file

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


if __name__ == '__main__':
    main()
