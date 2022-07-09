import sys
sys.dont_write_bytecode = True
from typing import Any
from threading import Thread

from spotipy import SpotifyException
from stopit import threading_timeoutable

from utils.timeout import raise_timeout
import globals


GET_LIBRARY_TIMEOUT = 16


# Each track is a dict with is_local, ID, and name
def get_simplified_tracks(playlist_id: str):
    simplified_tracks = []

    try:
        current_page = globals.SPOTIFY_API.playlist_items(f'spotify:playlist:{playlist_id}', fields='items.track.id,items.track.is_local,items.track.name,next')
    except SpotifyException as e:
        globals.HANDLE_SPOTIFY_EXCEPTION(e)

    while current_page:
        for item in current_page['items']:
            track = item['track']
            new_track = {}

            new_track['is_local'] = track['is_local']

            if not track['is_local']:
                new_track['id'] = track['id']
            else:
                new_track['id'] = None
            
            new_track['name'] = track['name']
            
            simplified_tracks.append(new_track)

        if current_page['next']:
            try:
                current_page = globals.SPOTIFY_API.next(current_page)
            except SpotifyException as e:
                globals.HANDLE_SPOTIFY_EXCEPTION(e)
            
        else:
            current_page = None
    
    return simplified_tracks

def store_simplified_tracks(library: dict, key: Any, playlist_id: str):
    library[key] = get_simplified_tracks(playlist_id)

@raise_timeout("!!! Timed out getting new libraries !!!")
@threading_timeoutable("TIMED OUT")
def get_libraries():
    threads = []

    try:
        current_page = globals.SPOTIFY_API.user_playlists(globals.LIBRARY_SPOTIFY_ACCOUNT_ID)
    except SpotifyException as e:
        globals.HANDLE_SPOTIFY_EXCEPTION(e)
    
    while current_page:
        for playlist in current_page["items"]:
            id = playlist["id"]
            name = playlist["name"]

            globals.PLAYLIST_ID_TO_NAME[id] = name

            if name.startswith("[G]"):
                thread = Thread(target=store_simplified_tracks, args=(globals.GENRES, id, id))
                thread.daemon = True
                thread.start()
                threads.append(thread)
            elif name.startswith("[AM]"):
                thread = Thread(target=store_simplified_tracks, args=(globals.ARCHIVED_MIXTAPES, id, id))
                thread.daemon = True
                thread.start()
                threads.append(thread)
            elif name.startswith("[AR]"):
                thread = Thread(target=store_simplified_tracks, args=(globals.ARCHIVED_RECORDS, id, id))
                thread.daemon = True
                thread.start()
                threads.append(thread)
            elif name.startswith("[1]"):
                thread = Thread(target=store_simplified_tracks, args=(globals.IMMEDIATE_TO_SORT, "tracks", id))
                thread.daemon = True
                thread.start()
                threads.append(thread)
            elif name.startswith("[2]"):
                thread = Thread(target=store_simplified_tracks, args=(globals.LIBRARY_TO_SORT, "tracks", id))
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
