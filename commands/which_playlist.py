import sys
sys.dont_write_bytecode = True
from difflib import get_close_matches

import globals
from utils.library_getter import *
from utils.library_tools import *


# Fetches the secondary-account playlists a given song link is contained within
def url_which(track_url: str):
    track_id = track_url.split("https://open.spotify.com/track/", 1)[1]

    containing_immediate_to_sort = None
    containing_library_to_sort = None
    containing_genres = []
    containing_archived_mixtapes = []
    contianing_archived_records = []

    for playlist_id, playlist_tracks in load_all_playlist_id_to_tracks().items():
        # If a playlist contains at least one track with a matching URL
        if [None for track in playlist_tracks if track["id"] == track_id] != []:
            playlist_name = globals.PLAYLIST_ID_TO_NAME[playlist_id]
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

def playlist_url_which(playlist_url: str):
    uri_and_si = playlist_url.split("https://open.spotify.com/playlist/", 1)[1]
    playlist_id = uri_and_si.split("?si=", 1)[0]
    tracks = [{"name": track["name"], "id": track["id"]} for track in get_simplified_tracks(playlist_id)]
    
    out_strings = []
    for track in tracks:
        out_strings.append(f"{track['name']}\n")
        for string in url_which(f"https://open.spotify.com/track/{track['id']}").split("\n"):
            out_strings.append(f"{string}\n")
        out_strings.append("\n\n")
    return "".join(out_strings)

# Fetches the secondary-account's closest-matching songs of a given song name and their containing playlists
def name_which(track_name: str, num_close_matches: int=5, cutoff: float=0.7):
    immediate_to_sort_close_matches = get_close_matches(track_name, [track["name"] for track in globals.IMMEDIATE_TO_SORT["tracks"]], num_close_matches, cutoff)
    library_to_sort_close_matches = get_close_matches(track_name, [track["name"] for track in globals.LIBRARY_TO_SORT["tracks"]], num_close_matches, cutoff)
    
    genres_close_matches = {}
    for id, tracks in globals.GENRES.items():
        genres_close_matches[id] = get_close_matches(track_name, [track["name"] for track in tracks], num_close_matches, cutoff)
    archived_mixtapes_close_matches = {}
    for id, tracks in globals.ARCHIVED_MIXTAPES.items():
        archived_mixtapes_close_matches[id] = get_close_matches(track_name, [track["name"] for track in tracks], num_close_matches, cutoff)
    archived_records_close_matches = {}
    for id, tracks in globals.ARCHIVED_RECORDS.items():
        archived_records_close_matches[id] = get_close_matches(track_name, [track["name"] for track in tracks], num_close_matches, cutoff)

    out_strings = []
    if immediate_to_sort_close_matches is not None:
        out_strings.append(f"{globals.IMMEDIATE_TO_SORT['name']}\n")
        for song in immediate_to_sort_close_matches:
            out_strings.append(f"    {song}\n")
        out_strings.append("\n")
    if library_to_sort_close_matches is not None:
        out_strings.append(f"{globals.LIBRARY_TO_SORT['name']}\n")
        for song in library_to_sort_close_matches:
            out_strings.append(f"    {song}\n")
        out_strings.append("\n")
    if genres_close_matches:
        out_strings.append("GENRES\n")
        for genre, close_matches in genres_close_matches.items():
            out_strings.append(f"    {genre}\n")
            for song in close_matches:
                out_strings.append(f"        {song}\n")
            out_strings.append("\n")
        out_strings.append("\n")
    if archived_mixtapes_close_matches:
        out_strings.append("ARCHIVED MIXTAPES\n")
        for archived_mixtape, close_matches in archived_mixtapes_close_matches.items():
            out_strings.append(f"    {archived_mixtape}\n")
            for song in close_matches:
                out_strings.append(f"        {song}\n")
            out_strings.append("\n")
        out_strings.append("\n")
    if archived_records_close_matches:
        out_strings.append("ARCHIVED RECORDS\n")
        for archived_record, close_matches in archived_records_close_matches.items():
            out_strings.append(f"    {archived_record}\n")
            for song in close_matches:
                out_strings.append(f"        {song}\n")
            out_strings.append("\n")
        out_strings.append("\n")
    return "".join(out_strings)