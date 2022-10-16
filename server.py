import sys
sys.dont_write_bytecode = True
from typing import Callable
from threading import Thread
from multiprocessing.connection import Listener

import globals
from utils.library_updater import *
from commands.which_playlist import *
from commands.add_to_playlist import *


SERVER = None

def send_output(command: Callable, *args, **kwargs):
    global SERVER
    print(f"Sending output of \'{command.__name__}\' command to client...")
    SERVER.send(command(*args, **kwargs))
    print(f"Output of \'{command.__name__}\' command sent to client")

def send_string(string):
    print("Sending string literal to client...")
    SERVER.send(string)
    print("String literal sent to client")

def server_listener_loop():
    global SERVER

    listener = Listener(globals.ADDRESS, authkey=globals.SOCKET_AUTHKEY)

    while True:
        print("Waiting on connection...")
        SERVER = listener.accept()
        print(f"Connection accepted from {listener.last_accepted}")

        message = None
        try:
            message = SERVER.recv()
        except EOFError:
            print(f"Connection from {listener.last_accepted} closed\n")
            continue
        
        command = message[0]
        arguments = message[1:]

        match command:
            case "url-which":
                track_url = arguments[0]
                send_output(url_which, track_url)
            case "playlist-url-which":
                playlist_url = arguments[0]
                send_output(playlist_url_which, playlist_url)
            case "name-which":
                track_name = arguments[0]
                send_output(name_which, track_name)
            case "url-add-to-immediate":
                track_url = arguments[0]
                send_output(url_add_to_immediate, track_url)
            
            case _:
                send_output(print, "ERROR: Unknown command-string identified in back-end")


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
        print("\nServer process terminated.")