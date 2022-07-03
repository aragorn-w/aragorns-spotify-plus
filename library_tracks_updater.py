# Background daemon process for continuously updating the saved JSONs of all the secondary Spotify account's playlists

from utils.library_loader import *


# Helper resources for updating the playlist library JSONs

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


if __name__ == '__main__':
    # Load in the saved playlist library JSONs as usable Python objects

    immediate_to_sort_tracks = load_library("immediate_to_sort_tracks")
    library_to_sort_tracks = load_library("library_to_sort_tracks")

    genre_id_to_tracks = load_library("genre_id_to_tracks")
    archived_mixtape_id_to_tracks = load_library("archived_mixtape_id_to_tracks")
    archived_record_id_to_tracks = load_library("archived_record_id_to_tracks")


    # Main loop for updating the saved playlist library JSONs

    while True:
        print("New library-update iteration...")

        _, immediate_to_sort_tracks = get_updated_playlist(globals.IMMEDIATE_TO_SORT_ID, immediate_to_sort_tracks, "immediate_to_sort_tracks")
        _, library_to_sort_tracks = get_updated_playlist(globals.LIBRARY_TO_SORT_ID, library_to_sort_tracks, "library_to_sort_tracks")

        update_playlist_folder(genre_id_to_tracks, "genre_id_to_tracks")
        update_playlist_folder(archived_mixtape_id_to_tracks, "archived_mixtape_id_to_tracks")
        update_playlist_folder(archived_record_id_to_tracks, "archived_record_id_to_tracks")