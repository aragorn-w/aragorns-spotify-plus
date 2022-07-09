import sys
sys.dont_write_bytecode = True
import json
from typing import Union
from time import time, sleep

import globals
from utils.library_getter import *


LIBRARY_UPDATE_PAUSE_TIME = 6


def save_library_as_JSON(JSON_name: str, library: Union[list, dict]):
    with open(f"saved_libraries/{JSON_name}.json", "w", encoding="utf-8") as outFile:
        json.dump(library, outFile, ensure_ascii=False, indent=4)

# Save most updated libraries tracks and namesto JSONs
def save_libraries():
    save_library_as_JSON("immediate_to_sort_tracks", globals.IMMEDIATE_TO_SORT["tracks"])
    save_library_as_JSON("library_to_sort_tracks", globals.LIBRARY_TO_SORT["tracks"])

    save_library_as_JSON("genre_id_to_tracks", globals.GENRES)
    save_library_as_JSON("archived_mixtape_id_to_tracks", globals.ARCHIVED_MIXTAPES)
    save_library_as_JSON("archived_record_id_to_tracks", globals.ARCHIVED_RECORDS)

    save_library_as_JSON("playlist_id_to_name", globals.PLAYLIST_ID_TO_NAME)

# Main loop for updating the saved playlist library JSONs
def update_library_tracks_loop(printout: bool=False):
    global LIBRARY_UPDATE_PAUSE_TIME, GET_LIBRARY_TIMEOUT

    running_times = []

    while True:
        total_start = time()

        if printout: print("\nNew library-update iteration...")

        if printout: print("Started getting new libraries...")
        start = time()
        
        get_libraries(timeout=GET_LIBRARY_TIMEOUT)
        if printout: print(f"Got new libraries ({round(time() - start, 3)}s)")

        if printout: print(f"Running manual API sleep for ({LIBRARY_UPDATE_PAUSE_TIME}s)...")
        sleep(LIBRARY_UPDATE_PAUSE_TIME)

        total_iteration_time = time() - total_start
        running_times.append(total_iteration_time)
        if printout: print(f"Finished loop iteration ({round(total_iteration_time, 3)}s)")
        if len(running_times) == 6:
            running_times.pop(0)
        if len(running_times) == 5:
            if printout: print(f"~~~5-point moving average ({round(sum(running_times)/5, 3)}s)~~~")