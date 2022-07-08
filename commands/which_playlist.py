import sys
sys.dont_write_bytecode = True
from difflib import get_close_matches

from spotipy import SpotifyException

import globals
from utils.library_getter import *


# Fetches the secondary-account playlists a given song link is contained within
def url_which(track_url: str):
    track_id = track_url[31:53]
    containing_playlists_id_to_name = []
    for playlist_id, playlist_tracks in load_all_playlist_id_to_tracks().items():
        if [None for track in playlist_tracks if track["id"] == track_id] != []:
            containing_playlists_id_to_name.append(playlist_id)
    
    containing_immediate_to_sort = None
    containing_library_to_sort = None
    containing_genres = []
    containing_archived_mixtapes = []
    contianing_archived_records = []

    for playlist_id in containing_playlists_id_to_name:
        try:
            response = globals.SPOTIFY_API.playlist(f"spotify:playlist:{playlist_id}", fields="name")
        except SpotifyException as e:
            globals.HANDLE_SPOTIFY_EXCEPTION(e)
            
        playlist_name = response["name"]
        if playlist_name.startswith("[1]"):
            containing_immediate_to_sort = playlist_name
        elif playlist_name.startswith("[2]"):
            containing_library_to_sort = playlist_name
        elif playlist_name.startswith("[G]"):
            containing_genres.append(playlist_name)
        elif playlist_name.startswith("[AM]"):
            containing_archived_mixtapes.append(playlist_name)
        elif playlist_name.startswith("[AR]"):
            contianing_archived_records.append(playlist_name)

    out_strings = []
    if containing_immediate_to_sort is not None:
        out_strings.append(f"{containing_immediate_to_sort}\n\n")
    if containing_library_to_sort is not None:
        out_strings.append(f"{containing_library_to_sort}\n\n")
    if containing_genres:
        out_strings.append("GENRES\n")
        for genre in containing_genres:
            out_strings.append(f"    {genre}\n")
        out_strings.append("\n")
    if containing_archived_mixtapes:
        out_strings.append("ARCHIVED MIXTAPES\n")
        for archived_mixtape in containing_archived_mixtapes:
            out_strings.append(f"    {archived_mixtape}\n")
        out_strings.append("\n")
    if contianing_archived_records:
        out_strings.append("ARCHIVED RECORDS\n")
        for archived_record in contianing_archived_records:
            out_strings.append(f"    {archived_record}\n")
        out_strings.append("\n")
    return "".join(out_strings)

def name_which(track_name: str, num_close_matches: int=5, cutoff: float=0.6):
    immediate_to_sort_close_matches = get_close_matches(track_name, [track["name"] for track in globals.IMMEDIATE_TO_SORT_TRACKS], num_close_matches, cutoff)
    library_to_sort_close_matches = get_close_matches(track_name, [track["name"] for track in globals.LIBRARY_TO_SORT_TRACKS], num_close_matches, cutoff)
    # genres_close_matches = {}
    # for genre_id in globals.GENRES:
    #     genres_close_matches[genre_id]


    '''
    track_id = track_url[31:53]
    containing_playlists_id_to_name = []
    for playlist_id, playlist_tracks in load_all_playlist_id_to_tracks().items():
        if [None for track in playlist_tracks if track["id"] == track_id] != []:
            containing_playlists_id_to_name.append(playlist_id)
    
    containing_immediate_to_sort = None
    containing_library_to_sort = None
    containing_genres = []
    containing_archived_mixtapes = []
    contianing_archived_records = []

    for playlist_id in containing_playlists_id_to_name:
        try:
            response = globals.SPOTIFY_API.playlist(f"spotify:playlist:{playlist_id}", fields="name")
        except SpotifyException as e:
            globals.HANDLE_SPOTIFY_EXCEPTION(e)
            
        playlist_name = response["name"]
        if playlist_name.startswith("[1]"):
            containing_immediate_to_sort = playlist_name
        elif playlist_name.startswith("[2]"):
            containing_library_to_sort = playlist_name
        elif playlist_name.startswith("[G]"):
            containing_genres.append(playlist_name)
        elif playlist_name.startswith("[AM]"):
            containing_archived_mixtapes.append(playlist_name)
        elif playlist_name.startswith("[AR]"):
            contianing_archived_records.append(playlist_name)

    out_strings = []
    if containing_immediate_to_sort is not None:
        out_strings.append(f"{containing_immediate_to_sort}\n\n")
    if containing_library_to_sort is not None:
        out_strings.append(f"{containing_library_to_sort}\n\n")
    if containing_genres:
        out_strings.append("GENRES\n")
        for genre in containing_genres:
            out_strings.append(f"    {genre}\n")
        out_strings.append("\n")
    if containing_archived_mixtapes:
        out_strings.append("ARCHIVED MIXTAPES\n")
        for archived_mixtape in containing_archived_mixtapes:
            out_strings.append(f"    {archived_mixtape}\n")
        out_strings.append("\n")
    if contianing_archived_records:
        out_strings.append("ARCHIVED RECORDS\n")
        for archived_record in contianing_archived_records:
            out_strings.append(f"    {archived_record}\n")
        out_strings.append("\n")
    return "".join(out_strings)
    '''