from os import getenv
import json
from threading import Thread

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Establish Spotify client credentials

CLIENT_CREDENTIALS_MANAGER = SpotifyClientCredentials(client_id=getenv('SPOTIFY_CLIENT_ID_1'), client_secret=getenv('SPOTIFY_CLIENT_SECRET_1'))
SPOTIFY_API = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS_MANAGER)

LIBRARY_SPOTIFY_ACCOUNT_ID = getenv('SPOTIFY_PLUS_SECONDARY_ACCOUNT_USER_ID')

API_SLEEP_TIME = 0

def assert_api_limit(response_dict):
    try:
        if response_dict["error"]["status"] == 429:
            print("!!! API rate limit exceeded !!!")
            assert 1 == 0
    except KeyError:
        pass


# Load the saved libraries

def load_library(library_name):
    library = None
    with open(f"saved_libraries/{library_name}.json", "r", encoding="utf-8") as file:
        library = json.load(file)
    return library

IMMEDIATE_TO_SORT_TRACKS = load_library("immediate_to_sort_tracks")
LIBRARY_TO_SORT_TRACKS = load_library("library_to_sort_tracks")

GENRES = load_library("genre_id_to_tracks")
ARCHIVED_MIXTAPES = load_library("archived_mixtape_id_to_tracks")
ARCHIVED_RECORDS = load_library("archived_record_id_to_tracks")


# Initialize the new libraries (but don't fetch)

NEW_IMMEDIATE_TO_SORT = ["06sD1Pm4x5hLo2gq9d8G6G", None]
NEW_LIBRARY_TO_SORT = ["2pdYtdLZcMLG6kAm7mRb4M", None]
NEW_GENRES = {}
NEW_ARCHIVED_MIXTAPES = {}
NEW_ARCHIVED_RECORDS = {}

# Each track is a dict with is_local, ID, and name
def get_simplified_tracks(playlist_id):
    global SPOTIFY_API

    simplified_tracks = []

    current_page = SPOTIFY_API.playlist_items(f'spotify:playlist:{playlist_id}', fields='items.track.id,items.track.is_local,items.track.name,next')
    assert_api_limit(current_page)

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
            current_page = SPOTIFY_API.next(current_page)
            assert_api_limit(current_page)
            
        else:
            current_page = None
    
    return simplified_tracks

def store_simplified_tracks(library, key, playlist_id):
    library[key] = get_simplified_tracks(playlist_id)

# OPTIMIZE: Figure out how the hell to speed this up (ex. multithreading, multiple clients, etc)
def get_libraries():
    global SPOTIFY_API, LIBRARY_SPOTIFY_ACCOUNT_ID
    
    global NEW_IMMEDIATE_TO_SORT, NEW_LIBRARY_TO_SORT, NEW_GENRES, NEW_ARCHIVED_MIXTAPES, NEW_ARCHIVED_RECORDS

    # Reset playlist folders so that library_tracks_updater can detect deleted playlists
    NEW_GENRES = {}
    NEW_ARCHIVED_MIXTAPES = {}
    NEW_ARCHIVED_RECORDS = {}

    threads = []

    current_page = SPOTIFY_API.user_playlists(LIBRARY_SPOTIFY_ACCOUNT_ID)
    assert_api_limit(current_page)
    while current_page:
        for playlist in current_page['items']:
            id = playlist['id']

            if playlist['name'].startswith('[G]'):
                thread = Thread(target=store_simplified_tracks, args=(NEW_GENRES, id, id))
                thread.start()
                threads.append(thread)
            elif playlist['name'].startswith('[AM]'):
                thread = Thread(target=store_simplified_tracks, args=(NEW_ARCHIVED_MIXTAPES, id, id))
                thread.start()
                threads.append(thread)
            elif playlist['name'].startswith('[AR]'):
                thread = Thread(target=store_simplified_tracks, args=(NEW_ARCHIVED_RECORDS, id, id))
                thread.start()
                threads.append(thread)
            elif playlist['name'].startswith('[1]'):
                NEW_IMMEDIATE_TO_SORT[0] = id
                thread = Thread(target=store_simplified_tracks, args=(NEW_IMMEDIATE_TO_SORT, 1, id))
                thread.start()
                threads.append(thread)
            elif playlist['name'].startswith('[2]'):
                NEW_LIBRARY_TO_SORT[0] = id 
                thread = Thread(target=store_simplified_tracks, args=(NEW_LIBRARY_TO_SORT, 1, id))
                thread.start()
                threads.append(thread)

        if current_page['next']:
            current_page = SPOTIFY_API.next(current_page)
            assert_api_limit(current_page)
        else:
            current_page = None
    
    for thread in threads:
        thread.join()