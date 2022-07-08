import sys
sys.dont_write_bytecode = True
from threading import Thread

from spotipy import SpotifyException

import globals


# Each track is a dict with is_local, ID, and name
def get_simplified_tracks(playlist_id):
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

def store_simplified_tracks(library, key, playlist_id):
    library[key] = get_simplified_tracks(playlist_id)

def get_libraries():
    globals.NEW_GENRES = {}
    globals.NEW_ARCHIVED_MIXTAPES = {}
    globals.NEW_ARCHIVED_RECORDS = {}

    threads = []

    try:
        current_page = globals.SPOTIFY_API.user_playlists(globals.LIBRARY_SPOTIFY_ACCOUNT_ID)
    except SpotifyException as e:
        globals.HANDLE_SPOTIFY_EXCEPTION(e)
    while current_page:
        for playlist in current_page['items']:
            id = playlist['id']

            if playlist['name'].startswith('[G]'):
                thread = Thread(target=store_simplified_tracks, args=(globals.NEW_GENRES, id, id))
                thread.start()
                threads.append(thread)
            elif playlist['name'].startswith('[AM]'):
                thread = Thread(target=store_simplified_tracks, args=(globals.NEW_ARCHIVED_MIXTAPES, id, id))
                thread.start()
                threads.append(thread)
            elif playlist['name'].startswith('[AR]'):
                thread = Thread(target=store_simplified_tracks, args=(globals.NEW_ARCHIVED_RECORDS, id, id))
                thread.start()
                threads.append(thread)
            elif playlist['name'].startswith('[1]'):
                thread = Thread(target=store_simplified_tracks, args=(globals.NEW_IMMEDIATE_TO_SORT, 1, id))
                thread.start()
                threads.append(thread)
            elif playlist['name'].startswith('[2]'):
                thread = Thread(target=store_simplified_tracks, args=(globals.NEW_LIBRARY_TO_SORT, 1, id))
                thread.start()
                threads.append(thread)

        if current_page['next']:
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
    
    all_playlist_id_to_tracks[globals.NEW_IMMEDIATE_TO_SORT[0]] = globals.IMMEDIATE_TO_SORT_TRACKS
    all_playlist_id_to_tracks[globals.NEW_LIBRARY_TO_SORT[0]] = globals.LIBRARY_TO_SORT_TRACKS

    all_playlist_id_to_tracks.update(globals.GENRES)
    all_playlist_id_to_tracks.update(globals.ARCHIVED_MIXTAPES)
    all_playlist_id_to_tracks.update(globals.ARCHIVED_RECORDS)

    return all_playlist_id_to_tracks

def playlists_are_equal(playlist1, playlist2):
    two_not_one = [track for track in playlist2 if track not in playlist1]
    one_not_two = [track for track in playlist1 if track not in playlist2]
    return two_not_one == [] and one_not_two == []
