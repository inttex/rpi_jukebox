import logging
from queue import Queue
from threading import Thread
from time import sleep

from rpi_jukebox.rfid_tools.rfid_thread import rfid_loop, reader_loop, switch_reader_loop


def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    logging.info('start')
    do_terminate_threads = False
    q = Queue()
    logging.info('starting threads')
    rfid_thread = Thread(target=rfid_loop, args=(q, lambda: do_terminate_threads))
    reader_thread = Thread(target=reader_loop, args=(q, lambda: do_terminate_threads, lambda _: print(_)))
    switch_reader_thread = Thread(target=switch_reader_loop, args=(lambda: do_terminate_threads, lambda _: print(_)))
    rfid_thread.start()
    reader_thread.start()
    switch_reader_thread.start()
    logging.info('sleeping')
    sleep(20)

    do_terminate_threads = True
    rfid_thread.join()
    reader_thread.join()
    switch_reader_thread.join()
