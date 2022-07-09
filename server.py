import sys
sys.dont_write_bytecode = True
from typing import Callable
from threading import Thread
from multiprocessing.connection import Listener

import globals
from utils.library_updater import *
from commands.which_playlist import *


CLIENT = None

def send_client(command: Callable, *args, **kwargs):
    global CLIENT
    print(f"Sending output of \'{command.__name__}\' command to client...")
    CLIENT.send(command(*args, **kwargs))
    print(f"Output of \'{command.__name__}\' command sent to client")

def server_listener_loop():
    global CLIENT

    listener = Listener(globals.ADDRESS, authkey=b"my secret password is this")

    while True:
        print("Waiting on connection...")
        CLIENT = listener.accept()
        print(f"Connection accepted from {listener.last_accepted}")

        message = None
        try:
            message = CLIENT.recv()
        except EOFError:
            print(f"Connection from {listener.last_accepted} closed\n")
            continue
        
        command = message[0]
        arguments = message[1:]

        if command == "url-which":
            track_url = arguments[0]
            send_client(url_which, track_url)
        elif command == "name-which":
            track_name = arguments[0]
            send_client(name_which, track_name)


if __name__ == "__main__":
    library_tracks_updater_thread = Thread(target=update_library_tracks_loop, kwargs={"printout": True})
    library_tracks_updater_thread.daemon = True
    library_tracks_updater_thread.start()

    server_listener_thread = Thread(target=server_listener_loop)
    server_listener_thread.daemon = True
    server_listener_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("!!! Keyboard interruption triggered !!!")
    finally:
        save_libraries()
        print("Libraries saved before exiting!")