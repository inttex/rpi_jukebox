import requests
from requests.exceptions import ConnectionError


def main():
    HOST = 'http://localhost:5000'
    api_communicator = APICommunicator(HOST)
    rfid = 1
    wav_file= api_communicator.get_music_file(rfid)
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

        :rfid:
        :returns: wav_file

        """

        wav_file = None

        url = self.url['jukebox'] + f'/{rfid}'
        try:
            rsp = requests.get(url)
        except ConnectionError:
            self._log_host_not_found()
        else:
            status = rsp.status_code
            if status == 404:
                self._create_new_resource(rfid)
            elif status == 200:
                wav_file = rsp.content
            else:
                print('did not get a answer')
                # logging.info('did not get a music, do nothing')
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

    def _create_new_resource(self, rfid):
        url = self.url['jukebox']
        rsp = requests.post(url, data={'rfid': rfid})
        # logging.info('create new entry point for this rfid')

    def _log_host_not_found(self):
            print('error:host not found')


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
                # logging.info('the music of play object no %s will be paused in %s s', play_obj.play_id, TIME)
        pass


if __name__ == '__main__':
    main()
