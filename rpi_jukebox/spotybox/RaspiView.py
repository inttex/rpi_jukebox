import logging
import traceback
from queue import Queue
from threading import Thread
from time import sleep
from typing import Callable

from RPi import GPIO
from rpi_jukebox.spotify_client.data_structs import SwitchState

from rpi_jukebox.rfid_tools.rfid_thread import rfid_loop, reader_loop, switch_reader_loop
from rpi_jukebox.spotybox.interfaces import ViewInterface, ControllerInterface


class RaspiView(ViewInterface):

    def __init__(self):
        self._do_terminate_threads = False
        q = Queue()
        self.rfid_thread = Thread(target=rfid_loop, args=(q, lambda: self._do_terminate_threads))
        self.reader_thread = Thread(target=reader_loop,
                                    args=(q, lambda: self._do_terminate_threads, self.rfid_callback))
        self.switch_reader_thread = Thread(target=switch_reader_loop,
                                           args=(lambda: self._do_terminate_threads, self.switch_callback))

        self._led_pin = 5

        self.led_thread = Thread(target=self.LED_loop, args=(lambda: self._do_terminate_threads,))

        self.init_LED()

    def LED_loop(self, is_do_terminate_threads: Callable):
        logging.info('starting led blink loop')
        try:
            while not is_do_terminate_threads():
                GPIO.output(self._led_pin, GPIO.HIGH)
                sleep(1)
                GPIO.output(self._led_pin, GPIO.LOW)
                sleep(1)

            logging.info('terminating led blink loop by flag')
        except:
            logging.info(('terminating led blink loop by exception', traceback.print_exc()))

    def set_controller(self, controller: ControllerInterface):
        self._controller = controller

    def rfid_callback(self, rfid_value: int):
        self._controller.evaluate_rfid(rfid_value)

    def switch_callback(self, new_switch_state: SwitchState):
        self._controller.evaluate_new_switch_state(new_switch_state)

    def run(self):
        GPIO.output(self._led_pin, GPIO.HIGH)
        self.rfid_thread.start()
        self.reader_thread.start()
        self.led_thread.start()
        self.switch_reader_thread.start()
        try:
            while not self._do_terminate_threads:
                sleep(0.1)

        finally:
            self.rfid_thread.join()
            self.reader_thread.join()
            self.led_thread.join()
            self.switch_reader_thread.join()
            logging.info('rfid and reader threads are successfully joined')

    def stop_view(self):
        logging.info('view: set terminate flag to True')
        self._do_terminate_threads = True
        GPIO.output(self._led_pin, GPIO.LOW)
        # GPIO.cleanup() # cleanup is done by rfid_thread

    def init_LED(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._led_pin, GPIO.OUT)
