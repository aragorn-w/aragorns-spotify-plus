import json

import globals


# Loader/Getter resources (getters involve Spotify Web API requests)

def load_library(library_name):
    library = None
    with open(f"saved_libraries/{library_name}.json", "r", encoding="utf-8") as file:
        library = json.load(file)
    return library

def load_all_playlist_id_to_tracks():
    all_playlist_id_to_tracks = {}
    
    all_playlist_id_to_tracks[globals.IMMEDIATE_TO_SORT_ID] = load_library("immediate_to_sort_tracks")
    all_playlist_id_to_tracks[globals.LIBRARY_TO_SORT_ID] = load_library("library_to_sort_tracks")

    all_playlist_id_to_tracks.update(load_library("genre_id_to_tracks"))
    all_playlist_id_to_tracks.update(load_library("archived_mixtape_id_to_tracks"))
    all_playlist_id_to_tracks.update(load_library("archived_record_id_to_tracks"))

    return all_playlist_id_to_tracks

# Each track is a dict with is_local, ID, and name
def get_simplified_tracks(playlist_id):
    simplified_tracks = []

    current_page = globals.SPOTIFY_API.playlist_items(f'spotify:playlist:{playlist_id}', fields='items.track.id,items.track.is_local,items.track.name,next')
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
            current_page = globals.SPOTIFY_API.next(current_page)
        else:
            current_page = None
    
    return simplified_tracks


# Operation resources

def playlists_are_equal(playlist1, playlist2):
    two_not_one = [track for track in playlist2 if track not in playlist1]
    one_not_two = [track for track in playlist1 if track not in playlist2]
    return two_not_one == [] and one_not_two == []
