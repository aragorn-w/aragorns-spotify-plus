import sys
sys.dont_write_bytecode = True
from threading import Thread

from library_tracks_updater import update_library_tracks


if __name__ == "__main__":
    library_tracks_updater = Thread(target=update_library_tracks)
    library_tracks_updater.start()
    