import sys
sys.dont_write_bytecode = True
from multiprocessing.connection import Client
import atexit

import typer

import globals


spotify_plus = typer.Typer()

CLIENT = None
if __name__ == "__main__":
    CLIENT = Client(globals.ADDRESS, authkey=globals.SOCKET_AUTHKEY)

# Fetches the secondary-account playlists a given track ID, from the track link, is contained within
@spotify_plus.command()
def uw(track_url: str):
    request_and_print("url-which", [track_url])

# Runs the URL-which command on each track of a given playlist
@spotify_plus.command()
def puw(playlist_url: str):
    request_and_print("playlist-url-which", [playlist_url])

# Fetches close-matching tracks, by name, and the containing playlists of said tracks
@spotify_plus.command()
def nw(track_name: str):
    request_and_print("name-which", [track_name])


def request_and_print(command: str, arguments: list[str]):
    global CLIENT
    CLIENT.send([command] + list(arguments))

    typer.echo(f"Awaiting server response for \'{command}\' command...\n")
    output = CLIENT.recv()
    typer.echo(output)

def close_connection():
    global CLIENT
    CLIENT.close()


if __name__ == "__main__":
    atexit.register(close_connection)
    spotify_plus()