from os import getenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Establish Spotify client credentials

CLIENT_CREDENTIALS_MANAGER = SpotifyClientCredentials(client_id=getenv('SPOTIPY_CLIENT_ID_CONTAINED_PLAYLISTS_FETCHER'), client_secret=getenv('SPOTIPY_CLIENT_SECRET_CONTAINED_PLAYLISTS_FETCHER'))
SPOTIFY_API = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS_MANAGER)

LIBRARY_SPOTIFY_ACCOUNT_ID = getenv('SPOTIFY_PLUS_SECONDARY_ACCOUNT_USER_ID')

IMMEDIATE_TO_SORT_ID = None
LIBRARY_TO_SORT_ID = None
GENRE_IDs = []
ARCHIVED_MIXTAPE_IDs = []
ARCHIVED_RECORD_IDs = []

def update_playlist_ids():    
    global IMMEDIATE_TO_SORT_ID, LIBRARY_TO_SORT_ID, GENRE_IDs, ARCHIVED_MIXTAPE_IDs, ARCHIVED_RECORD_IDs

    current_page = SPOTIFY_API.user_playlists(LIBRARY_SPOTIFY_ACCOUNT_ID)
    while current_page:
        for playlist in current_page['items']:
            id = playlist['id']

            if playlist['name'].startswith('[G]'):
                GENRE_IDs.append(id)
            elif playlist['name'].startswith('[AM]'):
                ARCHIVED_MIXTAPE_IDs.append(id)
            elif playlist['name'].startswith('[AR]'):
                ARCHIVED_RECORD_IDs.append(id)
            elif playlist['name'].startswith('[1]'):
                IMMEDIATE_TO_SORT_ID = id
            elif playlist['name'].startswith('[2]'):
                LIBRARY_TO_SORT_ID = id

        if current_page['next']:
            current_page = SPOTIFY_API.next(current_page)
        else:
            current_page = None
update_playlist_ids()