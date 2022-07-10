import sys
sys.dont_write_bytecode = True
import json
from typing import Union

import globals


def load_all_playlist_id_to_tracks():
    all_playlist_id_to_tracks = {}
    
    all_playlist_id_to_tracks[globals.IMMEDIATE_TO_SORT["id"]] = globals.IMMEDIATE_TO_SORT["tracks"]
    all_playlist_id_to_tracks[globals.LIBRARY_TO_SORT["id"]] = globals.LIBRARY_TO_SORT["tracks"]

    all_playlist_id_to_tracks.update(globals.GENRES)
    all_playlist_id_to_tracks.update(globals.ARCHIVED_MIXTAPES)
    all_playlist_id_to_tracks.update(globals.ARCHIVED_RECORDS)

    return all_playlist_id_to_tracks

def playlists_are_equal(playlist1: list[dict], playlist2: list[dict]):
    two_not_one = [track for track in playlist2 if track not in playlist1]
    one_not_two = [track for track in playlist1 if track not in playlist2]
    return two_not_one == [] and one_not_two == []

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