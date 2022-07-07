import sys
sys.dont_write_bytecode = True
from os import getenv
import json
from itertools import cycle

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Establish Spotify client credentials

NUM_CLIENTS = 6
API_POOL = cycle([spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=getenv(f"SPOTIFY_CLIENT_ID_{client_num}"), client_secret=getenv(f"SPOTIFY_CLIENT_SECRET_{client_num}"))) for client_num in range(1, NUM_CLIENTS, 1)])

def NEXT_API():
    return next(API_POOL)
NEXT_API()
NEXT_API()

LIBRARY_SPOTIFY_ACCOUNT_ID = getenv('SPOTIFY_PLUS_SECONDARY_ACCOUNT_USER_ID')

def ASSERT_API_LIMIT(response_dict):
    try:
        if response_dict["error"]["status"] == 429:
            print("!!! API rate limit exceeded !!!")
            assert 1 == 0
    except KeyError:
        pass


# Load the saved libraries

def LOAD_LIBRARY(library_name):
    library = None
    with open(f"saved_libraries/{library_name}.json", "r", encoding="utf-8") as file:
        library = json.load(file)
    return library

IMMEDIATE_TO_SORT_TRACKS = LOAD_LIBRARY("immediate_to_sort_tracks")
LIBRARY_TO_SORT_TRACKS = LOAD_LIBRARY("library_to_sort_tracks")

GENRES = LOAD_LIBRARY("genre_id_to_tracks")
ARCHIVED_MIXTAPES = LOAD_LIBRARY("archived_mixtape_id_to_tracks")
ARCHIVED_RECORDS = LOAD_LIBRARY("archived_record_id_to_tracks")


# Initialize the new libraries (but don't fetch)

NEW_IMMEDIATE_TO_SORT = ["06sD1Pm4x5hLo2gq9d8G6G", None]
NEW_LIBRARY_TO_SORT = ["2pdYtdLZcMLG6kAm7mRb4M", None]
NEW_GENRES = {}
NEW_ARCHIVED_MIXTAPES = {}
NEW_ARCHIVED_RECORDS = {}