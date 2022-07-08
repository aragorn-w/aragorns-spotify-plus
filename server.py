import sys
sys.dont_write_bytecode = True
from threading import Thread
from multiprocessing.connection import Listener

from library_tracks_updater import update_library_tracks
from commands.which_playlist import *


if __name__ == "__main__":
    address = ("localhost", 6163)
    listener = Listener(address, authkey=b"my secret password is this")

    library_tracks_updater = Thread(target=update_library_tracks, args=(True,))
    library_tracks_updater.start()

    while False:
        print("Waiting on connection...")
        client = listener.accept()
        print(f"Connection accepted from {listener.last_accepted}")

        message = None
        try:
            message = client.recv()
        except EOFError:
            print(f"Connection from {listener.last_accepted} closed\n")
            continue
        
        command = message[0]
        arguments = message[1:]

        if command == "url-which":
            track_url = arguments[0]
            print("Sending output of url-which command to client...")
            client.send(url_which(track_url))
            print("Output of url-which command sent to client")