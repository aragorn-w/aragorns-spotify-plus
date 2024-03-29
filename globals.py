import sys
sys.dont_write_bytecode = True
from os import getenv
import json

from spotipy import SpotifyException

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Spotify API stuff

CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
print(f"CLIENT_ID = {CLIENT_ID}")
SPOTIFY_API = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=getenv("SPOTIFY_CLIENT_SECRET")), requests_timeout=15, retries=5, status_retries=3, status_forcelist=(403, 404, 429, 500, 502, 503, 504))
LIBRARY_SPOTIFY_ACCOUNT_ID = getenv("SPOTIFY_SECONDARY_ACCOUNT_USER_ID")

def HANDLE_SPOTIFY_EXCEPTION(spotify_exception: SpotifyException):
    print(f"!!! SPOTIFY EXCEPTION: {spotify_exception.code} !!!")
    print(f"!!! Reason: {spotify_exception.reason} !!!")
    print(f"!!! Message: {spotify_exception.msg} !!!")
    assert 1 == 0


# Inter-process socket stuff

ADDRESS = ("localhost", int(getenv("SPOTIFY_PLUS_PORT")))
SOCKET_AUTHKEY = getenv("SPOTIFY_PLUS_AUTHKEY").encode()


# Saved library stuff

def LOAD_LIBRARY(library_name: str):
    library = None
    with open(f"saved_libraries/{library_name}.json", "r", encoding="utf-8") as file:
        library = json.load(file)
    return library

IMMEDIATE_TO_SORT = {"id": "06sD1Pm4x5hLo2gq9d8G6G", "tracks": LOAD_LIBRARY("immediate_to_sort_tracks"), "name": "[1] IMMEDIATE TO-SORT"}
LIBRARY_TO_SORT = {"id": "2pdYtdLZcMLG6kAm7mRb4M", "tracks": LOAD_LIBRARY("library_to_sort_tracks"), "name": "[2] LIBRARY TO-SORT"}

# id-->track list
GENRES = LOAD_LIBRARY("genre_id_to_tracks")
ARCHIVED_MIXTAPES = LOAD_LIBRARY("archived_mixtape_id_to_tracks")
ARCHIVED_RECORDS = LOAD_LIBRARY("archived_record_id_to_tracks")

# id-->playlist name
PLAYLIST_ID_TO_NAME = LOAD_LIBRARY("playlist_id_to_name")