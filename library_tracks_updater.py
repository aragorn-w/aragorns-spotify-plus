# Background daemon process for continuously updating the saved JSONs of all the secondary Spotify account's playlists

import sys
sys.dont_write_bytecode = True
import json
from time import time

from utils.library_loader import *


# Helper resources for updating the playlist library JSONs

def get_updated_playlist(tracks, new_tracks, playlist_json_name=None):
    if not playlists_are_equal(tracks, new_tracks):
        if playlist_json_name:
            with open(f"saved_libraries/{playlist_json_name}.json", "w", encoding="utf-8") as outFile:
                json.dump(new_tracks, outFile, ensure_ascii=False, indent=4)
        print("    New added/deleted playlist track(s) detected!")
        return True, new_tracks
    return False, new_tracks

def update_playlist_folder(playlist_id_to_tracks, new_playlist_id_to_tracks, playlist_folder_json_name):
    any_playlist_changed = False

    new_created_playlist_ids = set(new_playlist_id_to_tracks.keys())
    new_deleted_playlist_ids = []

    for playlist_id in playlist_id_to_tracks:
        # New library shows that playlist no longer exists
        if playlist_id not in new_playlist_id_to_tracks:
            print("    New deleted playlist(s) detected!")
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
        print("    New created playlist(s) detected!")
        for playlist_id in new_created_playlist_ids:
            playlist_id_to_tracks[playlist_id] = new_playlist_id_to_tracks[playlist_id]
        any_playlist_changed = True

    if any_playlist_changed:
        with open(f"saved_libraries/{playlist_folder_json_name}.json", "w", encoding="utf-8") as outFile:
            json.dump(new_playlist_id_to_tracks, outFile, ensure_ascii=False, indent=4)
        return True
    return False


if __name__ == '__main__':
    # Main loop for updating the saved playlist library JSONs

    running_times = []

    while True:
        total_start = time()

        print("\nNew library-update iteration...")

        print("Started getting new libraries...")
        start = time()
        get_libraries()
        print(f"Got new libraries ({round(time() - start, 3)}s)")

        _, globals.IMMEDIATE_TO_SORT_TRACKS = get_updated_playlist(globals.IMMEDIATE_TO_SORT_TRACKS, globals.NEW_IMMEDIATE_TO_SORT[1], "immediate_to_sort_tracks")
        # print("Finished updating IMMEDIATE TO-SORT")
        _, globals.LIBRARY_TO_SORT_TRACKS = get_updated_playlist(globals.LIBRARY_TO_SORT_TRACKS, globals.NEW_LIBRARY_TO_SORT[1], "library_to_sort_tracks")
        # print("Finished updating LIBRARY TO-SORT")

        update_playlist_folder(globals.GENRES, globals.NEW_GENRES, "genre_id_to_tracks")
        # print("Finished updating Genres")
        update_playlist_folder(globals.ARCHIVED_MIXTAPES, globals.NEW_ARCHIVED_MIXTAPES, "archived_mixtape_id_to_tracks")
        # print("Finished updating Archived Mixtapes")
        update_playlist_folder(globals.ARCHIVED_RECORDS, globals.NEW_ARCHIVED_RECORDS, "archived_record_id_to_tracks")
        # print("Finished updating Archived Records")

        total_iteration_time = time() - total_start
        running_times.append(total_iteration_time)
        print(f"Finished loop iteration ({round(total_iteration_time, 3)}s)")
        if len(running_times) == 6:
            running_times.pop(0)
        if len(running_times) == 5:
            print(f"~~~5-point moving average ({round(sum(running_times)/5, 3)}s)~~~")