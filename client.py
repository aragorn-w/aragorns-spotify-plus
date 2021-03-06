import sys
sys.dont_write_bytecode = True
from multiprocessing.connection import Client
import atexit

import typer

import globals


spotify_plus = typer.Typer()

SERVER = None
if __name__ == "__main__":
    SERVER = Client(globals.ADDRESS, authkey=globals.SOCKET_AUTHKEY)

# Fetches the secondary-account playlists a given track ID, from the track link, is contained within
@spotify_plus.command()
def uw(track_url: str):
    request_and_print("url-which", [track_url])

# Fetches close-matching tracks, by name, and the containing playlists of said tracks
@spotify_plus.command()
def nw(track_name: str):
    request_and_print("name-which", [track_name])


def request_and_print(command: str, arguments: list[str]):
    global SERVER
    SERVER.send([command] + list(arguments))

    typer.echo(f"Awaiting server response for \'{command}\' command...\n")
    output = SERVER.recv()
    typer.echo(output)

def close_connection():
    global SERVER
    SERVER.close()


if __name__ == "__main__":
    atexit.register(close_connection)
    spotify_plus()