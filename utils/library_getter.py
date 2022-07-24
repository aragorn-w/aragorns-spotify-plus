import sys
sys.dont_write_bytecode = True
from typing import Any
from threading import Thread

from spotipy import SpotifyException

import globals


GET_LIBRARY_TIMEOUT = 16


# Each track is a dict with is_local, ID, and name
def get_simplified_tracks(playlist_id: str):
    simplified_tracks = []

    try:
        current_page = globals.SPOTIFY_API.playlist_items(f"spotify:playlist:{playlist_id}", fields="items.track.id,items.track.is_local,items.track.name,next")
    except SpotifyException as e:
        globals.HANDLE_SPOTIFY_EXCEPTION(e)

    while current_page:
        for item in current_page["items"]:
            track = item["track"]
            new_track = {}

            new_track["is_local"] = track["is_local"]

            if not track["is_local"]:
                new_track["id"] = track["id"]
            else:
                new_track["id"] = None
            
            new_track["name"] = track["name"]
            
            simplified_tracks.append(new_track)

        if current_page["next"]:
            try:
                current_page = globals.SPOTIFY_API.next(current_page)
            except SpotifyException as e:
                globals.HANDLE_SPOTIFY_EXCEPTION(e)
            
        else:
            current_page = None
    
    return simplified_tracks

def store_simplified_tracks(library: dict, key: Any, playlist_id: str):
    if key == "tracks":
        library["id"] = playlist_id
        library["name"] = globals.PLAYLIST_ID_TO_NAME[playlist_id]
    library[key] = get_simplified_tracks(playlist_id)

def get_libraries():
    threads = []

    try:
        current_page = globals.SPOTIFY_API.user_playlists(globals.LIBRARY_SPOTIFY_ACCOUNT_ID)
    except SpotifyException as e:
        globals.HANDLE_SPOTIFY_EXCEPTION(e)
    
    # We go through the trouble of holding the API-gotten playlist data in staging variables so that any deleted playlists don't remain

    new_immediate_to_sort = {}
    new_library_to_sort = {}
    
    new_genres = {}
    new_archived_mixtapes = {}
    new_archived_records = {}

    new_playlist_id_to_name = {}

    while current_page:
        for playlist in current_page["items"]:
            id = playlist["id"]
            name = playlist["name"]

            new_playlist_id_to_name[id] = name

            if name.startswith("[1]"):
                thread = Thread(target=store_simplified_tracks, args=(new_immediate_to_sort, "tracks", id))
            elif name.startswith("[2]"):
                thread = Thread(target=store_simplified_tracks, args=(new_library_to_sort, "tracks", id))
            elif name.startswith("[G]"):
                thread = Thread(target=store_simplified_tracks, args=(new_genres, id, id))
            elif name.startswith("[AM]"):
                thread = Thread(target=store_simplified_tracks, args=(new_archived_mixtapes, id, id))
            elif name.startswith("[AR]"):
                thread = Thread(target=store_simplified_tracks, args=(new_archived_records, id, id))
            else:
                thread = None
            
            if thread:
                thread.daemon = True
                thread.start()
                threads.append(thread)

        if current_page["next"]:
            try:
                current_page = globals.SPOTIFY_API.next(current_page)
            except SpotifyException as e:
                globals.HANDLE_SPOTIFY_EXCEPTION(e)
        else:
            current_page = None
    
    for thread in threads:
        thread.join()
    
    globals.IMMEDIATE_TO_SORT = new_immediate_to_sort
    globals.LIBRARY_TO_SORT = new_library_to_sort

    globals.GENRES = new_genres
    globals.ARCHIVED_MIXTAPES = new_archived_mixtapes
    globals.ARCHIVED_RECORDS = new_archived_records

    globals.PLAYLIST_ID_TO_NAME = new_playlist_id_to_name