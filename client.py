import sys
sys.dont_write_bytecode = True
from multiprocessing.connection import Client
import atexit
from os import getenv

import typer

import globals
from utils.library_getter import *


spotify_plus = typer.Typer()

SERVER = None
if __name__ == "__main__":
    SERVER = Client(globals.ADDRESS, authkey=b"my secret password is this")

# Fetches the secondary-account playlists a given track ID, from the track link, is contained within
@spotify_plus.command()
def url_which(track_url: str):
    request_and_print("url-which", [track_url])

# Fetches close-matching tracks, by name, and the containing playlists of said tracks
@spotify_plus.command()
def name_which(track_name: str):
    request_and_print("name-which", [track_name])


def request_and_print(command: str, arguments: list[str]):
    global SERVER
    SERVER.send([command] + list(arguments))

    typer.echo(f"Awaiting server response for \'{command}\' command...")
    output = SERVER.recv()
    typer.echo(output)

def close_connection():
    global SERVER
    SERVER.close()


if __name__ == "__main__":
    atexit.register(close_connection)
    spotify_plus()