from difflib import get_close_matches

from utils.library_loader import *

import typer


spotify_plus = typer.Typer()

# Fetches the secondary-account playlists a given song link is contained within
@spotify_plus.command()
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
        response = globals.SPOTIFY_API.playlist(f"spotify:playlist:{playlist_id}", fields="name")
        globals.assert_api_limit(response)
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

    if containing_immediate_to_sort is not None:
        typer.echo(f"{containing_immediate_to_sort}\n")
    if containing_library_to_sort is not None:
        typer.echo(f"{containing_library_to_sort}\n")
    if containing_genres:
        typer.echo("GENRES")
        for genre in containing_genres:
            typer.echo(f"    {genre}")
        typer.echo()
    if containing_archived_mixtapes:
        typer.echo("ARCHIVED MIXTAPES")
        for archived_mixtape in containing_archived_mixtapes:
            typer.echo(f"    {archived_mixtape}")
        typer.echo()
    if contianing_archived_records:
        typer.echo("ARCHIVED RECORDS")
        for archived_record in contianing_archived_records:
            typer.echo(f"    {archived_record}")
        typer.echo()

@spotify_plus.command()
def song_which(song_name: str):
    NUM_CLOSE_MATCHES = 5
    CUTOFF = 0.6

    # immediate_to_sort_close_matches = get_close_matches(song_name, )

    # containing_playlists_id_to_name = []
    # for playlist_id, playlist_tracks in load_all_playlist_id_to_tracks().items():
    #     if [None for track in playlist_tracks if track["id"] == track_id] != []:
    #         containing_playlists_id_to_name.append(playlist_id)
    
    # containing_immediate_to_sort = None
    # containing_library_to_sort = None
    # containing_genres = []
    # containing_archived_mixtapes = []
    # contianing_archived_records = []

    # for playlist_id in containing_playlists_id_to_name:
    #     playlist_name = SPOTIFY_API.playlist(f"spotify:playlist:{playlist_id}", fields="name")["name"]
    #     if playlist_name.startswith("[1]"):
    #         containing_immediate_to_sort = playlist_name
    #     elif playlist_name.startswith("[2]"):
    #         containing_library_to_sort = playlist_name
    #     elif playlist_name.startswith("[G]"):
    #         containing_genres.append(playlist_name)
    #     elif playlist_name.startswith("[AM]"):
    #         containing_archived_mixtapes.append(playlist_name)
    #     elif playlist_name.startswith("[AR]"):
    #         contianing_archived_records.append(playlist_name)

    # if containing_immediate_to_sort is not None:
    #     typer.echo(f"{containing_immediate_to_sort}\n")
    # if containing_library_to_sort is not None:
    #     typer.echo(f"{containing_library_to_sort}\n")
    # if containing_genres:
    #     typer.echo("GENRES")
    #     for genre in containing_genres:
    #         typer.echo(f"    {genre}")
    #     typer.echo()
    # if containing_archived_mixtapes:
    #     typer.echo("ARCHIVED MIXTAPES")
    #     for archived_mixtape in containing_archived_mixtapes:
    #         typer.echo(f"    {archived_mixtape}")
    #     typer.echo()
    # if contianing_archived_records:
    #     typer.echo("ARCHIVED RECORDS")
    #     for archived_record in contianing_archived_records:
    #         typer.echo(f"    {archived_record}")
    #     typer.echo()


if __name__ == "__main__":
    spotify_plus()