from os import getenv
import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Establish Spotify client credentials

client_credentials_manager = SpotifyClientCredentials(client_id=getenv('SPOTIPY_CLIENT_ID_CONTAINED_PLAYLISTS_FETCHER'), client_secret=getenv('SPOTIPY_CLIENT_SECRET_CONTAINED_PLAYLISTS_FETCHER'))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

library_account = getenv('SPOTIFY_PLUS_SECONDARY_ACCOUNT_USER_ID')


# Helper resources for loading in the playlist library JSONs

def load_library(library_name):
    library = None
    with open(f"saved_libraries/{library_name}.json", "r", encoding="utf-8") as file:
        library = json.load(file)
    return library


# Helper resources for requesting the Spotify playlists and updating the playlist library JSONs

def get_simplified_tracks(playlist_id):
    simplified_tracks = []

    current_page = sp.playlist_items(f'spotify:playlist:{playlist_id}', fields='items.track.id,items.track.is_local,items.track.name,next')
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
            current_page = sp.next(current_page)
        else:
            current_page = None
    
    return simplified_tracks

def playlists_are_equal(playlist1, playlist2):
    two_not_one = [track for track in playlist2 if track not in playlist1]
    one_not_two = [track for track in playlist1 if track not in playlist2]
    return two_not_one == [] and one_not_two == []

def get_updated_playlist(playlist_id, playlist_tracks, playlist_json_name=None):
    new_playlist_tracks = get_simplified_tracks(playlist_id)
    # Optimization note: Finding changes to a playlist
    if not playlists_are_equal(playlist_tracks, new_playlist_tracks):        
        if playlist_json_name:
            with open(f"saved_libraries/{playlist_json_name}.json", "w", encoding="utf-8") as outFile:
                json.dump(playlist_tracks, outFile, ensure_ascii=False, indent=4)
        
        return True, new_playlist_tracks
    return False, new_playlist_tracks

def update_playlist_folder(playlist_id_to_tracks, playlist_folder_json_name):
    any_playlist_changed = False

    for playlist_id in playlist_id_to_tracks:
        playlist_updated, new_playlist = get_updated_playlist(playlist_id, playlist_id_to_tracks[playlist_id])
        any_playlist_changed = any_playlist_changed or playlist_updated

        if playlist_updated:
            playlist_id_to_tracks[playlist_id] = new_playlist
    
    if any_playlist_changed:
        with open(f"saved_libraries/{playlist_folder_json_name}.json", "w", encoding="utf-8") as outFile:
            json.dump(playlist_id_to_tracks, outFile, ensure_ascii=False, indent=4)
        return True
    return False


# Get all playlist IDs

immediate_to_sort_id = ''
library_to_sort_id = ''

genre_ids = []
archived_mixtape_ids = []
archived_record_ids = []

current_page = sp.user_playlists(library_account)
while current_page:
    for playlist in current_page['items']:
        id = playlist['id']

        if playlist['name'].startswith('[G]'):
            genre_ids.append(id)
        elif playlist['name'].startswith('[AM]'):
            archived_mixtape_ids.append(id)
        elif playlist['name'].startswith('[AR]'):
            archived_record_ids.append(id)
        elif playlist['name'].startswith('[1]'):
            immediate_to_sort_id = id
        elif playlist['name'].startswith('[2]'):
            library_to_sort_id = id

    if current_page['next']:
        current_page = sp.next(current_page)
    else:
        current_page = None


# Load in the saved playlist library JSONs as usable Python objects

immediate_to_sort_tracks = load_library("immediate_to_sort_tracks")
library_to_sort_tracks = load_library("library_to_sort_tracks")

genre_id_to_tracks = load_library("genre_id_to_tracks")
archived_mixtape_id_to_tracks = load_library("archived_mixtape_id_to_tracks")
archived_record_id_to_tracks = load_library("archived_record_id_to_tracks")


# Main loop for updating the saved playlist library JSONs

while True:
    print("New iteration")

    _, immediate_to_sort_tracks = get_updated_playlist(immediate_to_sort_id, immediate_to_sort_tracks, "immediate_to_sort_tracks")
    _, library_to_sort_tracks = get_updated_playlist(library_to_sort_id, library_to_sort_tracks, "library_to_sort_tracks")

    update_playlist_folder(genre_id_to_tracks, "genre_id_to_tracks")
    update_playlist_folder(archived_mixtape_id_to_tracks, "archived_mixtape_id_to_tracks")
    update_playlist_folder(archived_record_id_to_tracks, "archived_record_id_to_tracks")