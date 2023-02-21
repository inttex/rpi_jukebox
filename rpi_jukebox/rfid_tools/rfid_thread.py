import datetime
import logging
import traceback
from queue import Queue
from threading import Thread
from time import sleep
from typing import Callable

from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

from rpi_jukebox.spotify_client.data_structs import SwitchState

MIN_DELAY_RFID_SEC = 2


def send_rfid_to_q(rfid_result, q: Queue):
    if q.full():
        q.get()
    q.put(rfid_result)


def rfid_loop(q: Queue, is_do_terminate_threads):
    logging.info('starting rfid_loop')
    try:
        reader = SimpleMFRC522()
        last_valid_id = None
        timestamp_of_last_valid = datetime.datetime.now()
        while not is_do_terminate_threads():
            id, text = reader.read_no_block()
            # print('\t', id, text)
            sleep(0.05)
            if id != None:
                now = datetime.datetime.now()
                # print('found id',id)
                if id != last_valid_id:
                    send_rfid_to_q((id, text), q)
                    timestamp_of_last_valid = now
                    last_valid_id = id
                else:  # check wether to re-inject this rfid tag
                    if (now - timestamp_of_last_valid).total_seconds() > MIN_DELAY_RFID_SEC:
                        send_rfid_to_q((id, text), q)
                        timestamp_of_last_valid = now
                        last_valid_id = id
        logging.info('terminating rfid_loop by flag')
    except:
        logging.info(('terminating rfid_loop by exception', traceback.print_exc()))
    finally:
        # GPIO.cleanup()
        GPIO.setwarnings(False)
        logging.info('cleanup GPIOs')


def reader_loop(q: Queue, is_do_terminate_threads: Callable, rfid_callback: Callable):
    logging.info('starting reader_loop')
    try:
        while not is_do_terminate_threads():
            if not q.empty():
                key, text = q.get()
                logging.debug('received rfid %s' % key)
                rfid_callback(key)

            sleep(0.1)
        logging.info('terminating reader_loop by flag')
    except:
        logging.info(('terminating reader_loop by exception', traceback.print_exc()))


def switch_reader_loop(is_do_terminate_threads: Callable, switch_callback: Callable):
    logging.info('starting switch reader_loop')
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        last_switch_state = False
        while not is_do_terminate_threads():
            sleep(0.1)
            if GPIO.input(10):
                current_switch_state = SwitchState.INTERNAL
            else:
                current_switch_state = SwitchState.EXTERNAL
            if current_switch_state != last_switch_state:
                switch_callback(current_switch_state)
                logging.info('new switch state %s' % current_switch_state)
                last_switch_state = current_switch_state

        logging.info('terminating switch reader_loop by flag')
    except:
        logging.info(('terminating switch reader_loop by exception', traceback.print_exc()))


def main():
    do_terminate_threads = False
    q = Queue()
    rfid_thread = Thread(target=rfid_loop, args=(q, lambda: do_terminate_threads))
    reader_thread = Thread(target=reader_loop, args=(q, lambda: do_terminate_threads))

    sleep(20)

    do_terminate_threads = True
    rfid_thread.join()
    reader_thread.join()


if __name__ == '__main__':
    main()
