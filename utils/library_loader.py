import sys
sys.dont_write_bytecode = True

import globals


def load_all_playlist_id_to_tracks():
    all_playlist_id_to_tracks = {}
    
    all_playlist_id_to_tracks[globals.NEW_IMMEDIATE_TO_SORT[0]] = globals.IMMEDIATE_TO_SORT_TRACKS
    all_playlist_id_to_tracks[globals.NEW_LIBRARY_TO_SORT[0]] = globals.LIBRARY_TO_SORT_TRACKS

    all_playlist_id_to_tracks.update(globals.GENRES)
    all_playlist_id_to_tracks.update(globals.ARCHIVED_MIXTAPES)
    all_playlist_id_to_tracks.update(globals.ARCHIVED_RECORDS)

    return all_playlist_id_to_tracks

def playlists_are_equal(playlist1, playlist2):
    two_not_one = [track for track in playlist2 if track not in playlist1]
    one_not_two = [track for track in playlist1 if track not in playlist2]
    return two_not_one == [] and one_not_two == []
