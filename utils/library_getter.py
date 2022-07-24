import sys
sys.dont_write_bytecode = True
from threading import Thread
from queue import Queue

from spotipy import SpotifyException

import globals


GET_LIBRARY_TIMEOUT = 16


# Each track is a dict with is_local, ID, and name
def get_simplified_tracks(playlist_id: str):
    simplified_tracks = []

    try:
        current_page = globals.SPOTIFY_API.playlist_items(f"spotify:playlist:{playlist_id}", fields="items.track.id,items.track.is_local,items.track.name,next")
    except SpotifyException as e:
        globals.HANDLE_SPOTIFY_EXCEPTION(e)

    while current_page:
        for item in current_page["items"]:
            track = item["track"]
            new_track = {}

            new_track["is_local"] = track["is_local"]

            if not track["is_local"]:
                new_track["id"] = track["id"]
            else:
                new_track["id"] = None
            
            new_track["name"] = track["name"]
            
            simplified_tracks.append(new_track)

        if current_page["next"]:
            try:
                current_page = globals.SPOTIFY_API.next(current_page)
            except SpotifyException as e:
                globals.HANDLE_SPOTIFY_EXCEPTION(e)
            
        else:
            current_page = None
    
    return simplified_tracks

# def store_simplified_tracks(library: dict, key: Any, playlist_id: str):
#     if key == "tracks":
#         library["id"] = playlist_id
#         library["name"] = globals.PLAYLIST_ID_TO_NAME[playlist_id]
#     library[key] = get_simplified_tracks(playlist_id)

def get_libraries_crawl(queue: Queue, results: dict[str, dict]):
    while not queue.empty():
        library_name, key, playlist_id = queue.get()
        
        if library_name.startswith("[1]"):
            target_result = results["immediate_to_sort"]
        elif library_name.startswith("[2]"):
            target_result = results["library_to_sort"]
        elif library_name.startswith("[G]"):
            target_result = results["genres"]
        elif library_name.startswith("[AM]"):
            target_result = results["archived_mixtapes"]
        elif library_name.startswith("[AR]"):
            target_result = results["archived_records"]
        
        if key == "tracks":
            target_result["id"] = playlist_id
            target_result["name"] = globals.PLAYLIST_ID_TO_NAME[playlist_id]

        target_result[key] = get_simplified_tracks(playlist_id)

        queue.task_done()
    return True

def get_libraries():
    # We go through the trouble of holding the API-gotten playlist data in staging variables so that any deleted playlists don't remain

    new_playlist_id_to_name = {}

    queue = Queue()
    results = {"immediate_to_sort": {}, "library_to_sort": {}, "genres": {}, "archived_mixtapes": {}, "archived_records": {}}
    
    while current_page:
        for playlist in current_page["items"]:
            id = playlist["id"]
            name = playlist["name"]

            new_playlist_id_to_name[id] = name

            if name.startswith("[1]") or name.startswith("[2]"):
                queue.put((name, "tracks", id))
            elif name.startswith("[G]") or name.startswith("[AM]") or name.startswith("[AR]"):
                queue.put((name, id, id))

        if current_page["next"]:
            try:
                current_page = globals.SPOTIFY_API.next(current_page)
            except SpotifyException as e:
                globals.HANDLE_SPOTIFY_EXCEPTION(e)
        else:
            current_page = None
    
    globals.PLAYLIST_ID_TO_NAME = new_playlist_id_to_name

    for _ in range(len(new_playlist_id_to_name)):
        worker = Thread(target=get_libraries_crawl, args=(queue, results))
        worker.daemon = True
        worker.start()

    queue.join()
    
    globals.IMMEDIATE_TO_SORT = results["immediate_to_sort"]
    globals.LIBRARY_TO_SORT = results["library_to_sort"]

    globals.GENRES = results["genres"]
    globals.ARCHIVED_MIXTAPES = results["archived_mixtapes"]
    globals.ARCHIVED_RECORDS = results["archived_records"]