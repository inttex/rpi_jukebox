import os
import random
import warnings
import logging


import requests
from requests.exceptions import ConnectionError
with warnings.catch_warnings():
    warnings.simplefilter('ignore', category=RuntimeWarning)
    from pydub import AudioSegment


from rpi_jukebox.api.config import default_parameters


def main():
    test_music_loader()


def test_api_comm_param():
    HOST = 'http://localhost:5000/'
    api_communicator = APICommunicator(HOST)
    parameter = api_communicator.get_parameter('tmin')
    print(parameter, type(parameter))
    parameter = api_communicator.get_parameter('tmax')
    print(parameter, type(parameter))
    parameter = api_communicator.get_parameter('random_stop')
    print(parameter, type(parameter))
    wav_file = api_communicator.get_music_file(2)
    print(type(wav_file))


def test_music_loader():
    mu = MusicLoader()
    start_times = mu._create_start_times(30000, 3000, 10000)
    print(start_times)
    HOST = 'http://localhost:5000/'
    api_communicator = APICommunicator(HOST)
    wav_file = api_communicator.get_music_file(2)
    mu.random_stop = True
    mu.tmax_ms = 30000
    mu.tmin_ms = 5000
    seg = mu.get_sound(wav_file)
    print(seg)
    print(len(seg))
    for i in range(10):
        seg = mu.get_sound(None)
        print(seg)
        print(len(seg))


class APICommunicator(object):

    """communicate by requests to the api restless server"""
    _entry_points = {'jukebox': 'jukebox'}
    _default_values = default_parameters
    for name in _default_values:
        _entry_points[name] = f'parameters/{name}'

    def __init__(self, host):
        self._host = host
        self._url = {
                name: self._host + entry
                for name, entry in self._entry_points.items()}

    def get_music_file(self, rfid):
        """obtain wav file from server

        :rfid:
        :returns: wav_file

        """

        wav_file = None

        url = self._url['jukebox'] + f'/{rfid}'
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
                logging.info('did not get a music, do nothing')
        return wav_file

    def get_parameter(self, parameter_name):
        """get a parameter from api

        :returns: parameter value

        """
        parameter_value = self._default_values[parameter_name]

        url = self._url[parameter_name]
        try:
            rsp = requests.get(url)
        except ConnectionError:
            self._log_host_not_found()
        else:
            status = rsp.status_code
            if status == 200:
                parameter_value = rsp.json()
            else:
                self._log_parameter_error(parameter_name, status)
        return parameter_value

    def _create_new_resource(self, rfid):
        url = self._url['jukebox']
        rsp = requests.post(url, data={'rfid': rfid})
        if rsp.ok:
            logging.info('new resource created for rfid %s', rfid)
        else:
            logging.error(
                    'failed to create new resource'
                    ' for rfid %s. status code=%s',
                    rfid, rsp.status_code)

    def _log_host_not_found(self):
        logging.error('host not found')

    def _log_parameter_error(self, parameter_name, status_code):
        logging.error(
                'I got status code %s from the API after asking'
                'for the value of parameter %s.'
                'I used the default value.',
                status_code, parameter_name)


class MusicLoader(object):

    """prepare the segment of music to be played"""

    def __init__(self):
        self.rfid = None
        self.random_stop = None
        self.tmin_ms = None
        self.tmax_ms = None
        self._song = None
        self._start_times = None
        self._start_time_index = None
        self.volume_increase_dB = 0

    def get_sound(self, wav_file):
        if wav_file is not None:
            with open('temp.wav', 'wb') as myfile:
                myfile.write(wav_file)
            self._song = AudioSegment.from_wav('temp.wav')
            os.remove('temp.wav')
            self._start_times = None

        if self._start_times is None:
            if self.random_stop:
                self._start_times = self._create_start_times(
                        len(self._song),
                        self.tmin_ms,
                        self.tmax_ms,
                        )
            else:
                self._start_times = [0]
            self._start_time_index = 0
        logging.info('segment %s/%s', self._start_time_index+1, len(self._start_times))

        t1 = self._start_times[self._start_time_index]
        if self._start_time_index < len(self._start_times)-1:
            t2 = self._start_times[self._start_time_index + 1]
            self._start_time_index += 1
        else:
            t2 = None
            self._start_times = None

        audio_segment = self._song[t1:t2]

        return audio_segment + self.volume_increase_dB

    def _create_start_times(self, total_length: int, tmin: int, tmax: int):
        """create random start times of random length between tmin and tmax

        :total_length: of audio segment (ms)
        :tmin: in ms
        :tmax: ms
        :returns: list of int start times

        """
        start_times = [0]
        while total_length - start_times[-1] > tmax:
            T = random.randint(tmin, tmax)
            start_times.append(start_times[-1] + T)
        return start_times


if __name__ == '__main__':
    main()
