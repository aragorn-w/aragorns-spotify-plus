import sys
sys.dont_write_bytecode = True
import json
from time import time, sleep

import globals
from utils.library_getter import *


LIBRARY_UPDATE_PAUSE_TIME = 6


# Helper resources for updating the playlist library JSONs

def get_updated_playlist(tracks, new_tracks, playlist_json_name=None, printout=False):
    if not playlists_are_equal(tracks, new_tracks):
        if playlist_json_name:
            with open(f"saved_libraries/{playlist_json_name}.json", "w", encoding="utf-8") as outFile:
                json.dump(new_tracks, outFile, ensure_ascii=False, indent=4)
        if printout: print("    New added/deleted playlist track(s) detected!")
        return True, new_tracks
    return False, new_tracks

def update_playlist_folder(playlist_id_to_tracks, new_playlist_id_to_tracks, playlist_folder_json_name, printout=False):
    any_playlist_changed = False

    new_created_playlist_ids = set(new_playlist_id_to_tracks.keys())
    new_deleted_playlist_ids = []

    for playlist_id in playlist_id_to_tracks:
        # New library shows that playlist no longer exists
        if playlist_id not in new_playlist_id_to_tracks:
            if printout: print("    New deleted playlist(s) detected!")
            new_deleted_playlist_ids.append(playlist_id)
            any_playlist_changed = True
            continue

        new_created_playlist_ids.remove(playlist_id)

        playlist_updated, new_tracks = get_updated_playlist(playlist_id_to_tracks[playlist_id], new_playlist_id_to_tracks[playlist_id])
        any_playlist_changed = any_playlist_changed or playlist_updated

        if playlist_updated:
            playlist_id_to_tracks[playlist_id] = new_tracks
    
    for playlist_id in new_deleted_playlist_ids:
        playlist_id_to_tracks.pop(playlist_id)

    if new_created_playlist_ids:
        if printout: print("    New created playlist(s) detected!")
        for playlist_id in new_created_playlist_ids:
            playlist_id_to_tracks[playlist_id] = new_playlist_id_to_tracks[playlist_id]
        any_playlist_changed = True

    if any_playlist_changed:
        with open(f"saved_libraries/{playlist_folder_json_name}.json", "w", encoding="utf-8") as outFile:
            json.dump(new_playlist_id_to_tracks, outFile, ensure_ascii=False, indent=4)
        return True
    return False

def update_library_tracks_loop(printout=False):
    # Main loop for updating the saved playlist library JSONs

    global LIBRARY_UPDATE_PAUSE_TIME, GET_LIBRARY_TIMEOUT

    running_times = []

    while True:
        total_start = time()

        if printout: print("\nNew library-update iteration...")

        if printout: print("Started getting new libraries...")
        start = time()
        
        if get_libraries(timeout=GET_LIBRARY_TIMEOUT) == "TIMED OUT":
            raise Exception("!!! Timed out getting new libraries !!!")
        if printout: print(f"Got new libraries ({round(time() - start, 3)}s)")

        _, globals.IMMEDIATE_TO_SORT_TRACKS = get_updated_playlist(globals.IMMEDIATE_TO_SORT_TRACKS, globals.NEW_IMMEDIATE_TO_SORT[1], "immediate_to_sort_tracks", printout)
        # if printout: print("Finished updating IMMEDIATE TO-SORT")
        _, globals.LIBRARY_TO_SORT_TRACKS = get_updated_playlist(globals.LIBRARY_TO_SORT_TRACKS, globals.NEW_LIBRARY_TO_SORT[1], "library_to_sort_tracks", printout)
        # if printout: print("Finished updating LIBRARY TO-SORT")

        update_playlist_folder(globals.GENRES, globals.NEW_GENRES, "genre_id_to_tracks", printout)
        # if printout: print("Finished updating Genres")
        update_playlist_folder(globals.ARCHIVED_MIXTAPES, globals.NEW_ARCHIVED_MIXTAPES, "archived_mixtape_id_to_tracks", printout)
        # if printout: print("Finished updating Archived Mixtapes")
        update_playlist_folder(globals.ARCHIVED_RECORDS, globals.NEW_ARCHIVED_RECORDS, "archived_record_id_to_tracks", printout)
        # if printout: print("Finished updating Archived Records")

        if printout: print(f"Running manual API sleep for ({LIBRARY_UPDATE_PAUSE_TIME}s)...")
        sleep(LIBRARY_UPDATE_PAUSE_TIME)

        total_iteration_time = time() - total_start
        running_times.append(total_iteration_time)
        if printout: print(f"Finished loop iteration ({round(total_iteration_time, 3)}s)")
        if len(running_times) == 6:
            running_times.pop(0)
        if len(running_times) == 5:
            if printout: print(f"~~~5-point moving average ({round(sum(running_times)/5, 3)}s)~~~")