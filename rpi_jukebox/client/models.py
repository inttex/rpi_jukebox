import requests
from requests.exceptions import ConnectionError


def main():
    HOST = 'http://localhost:5000'
    api_communicator = APICommunicator(HOST)
    parameter = api_communicator.get_parameter('random_stop')
    print(parameter)
    parameter = api_communicator.get_parameter('tmin')
    print(parameter)
    parameter = api_communicator.get_parameter('tmax')
    print(parameter)
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
    default_values = dict(
            random_stop=False,
            tmin=5,
            tmax=20,
            )

    def __init__(self, host):
        """TODO: to be defined. """
        self.host = host
        self.url = {
                name: f'{self.host}/{entry}'
                for name, entry in self.entry_points.items()}

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
                print('did not get a music')
                # logging.info('did not get a music, do nothing')
        return wav_file

    def get_parameter(self, parameter_name):
        """get a parameter from api

        :returns: parameter value

        """
        parameter_value = self.default_values[parameter_name]

        url = self.url[parameter_name]
        try:
            rsp = requests.get(url)
        except ConnectionError:
            self._log_host_not_found()
        else:
            status = rsp.status_code
            if status == 200:
                parameter_value = rsp.content
            else:
                self._log_parameter_error(parameter_name, status)
        return parameter_value

    def _create_new_resource(self, rfid):
        url = self.url['jukebox']
        requests.post(url, data={'rfid': rfid})
        # logging.info('create new entry point for this rfid')

    def _log_host_not_found(self):
        print('error:host not found')

    def _log_parameter_error(self, parameter_name, status_code):
        msg = (
                f'I got status code {status_code} from the API after asking'
                f'for the value of parameter {parameter_name}.'
                'I used the default value.')
        print(msg)


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
