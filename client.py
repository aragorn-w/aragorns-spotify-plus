import sys
sys.dont_write_bytecode = True
from difflib import get_close_matches
from multiprocessing.connection import Client
import atexit

import typer

from globals import *
from utils.library_loader import *


spotify_plus = typer.Typer()

ADDRESS = ("localhost", 6163)
SERVER = None
if __name__ == "__main__":
    SERVER = Client(ADDRESS, authkey=b"my secret password is this")

# Fetches the secondary-account playlists a given song link is contained within
@spotify_plus.command()
def url_which(track_url: str):
    global SERVER
    SERVER.send(["url-which"] + list(track_url))

    typer.echo(f"Awaiting server response for command...")
    output = SERVER.recv()
    typer.echo(output)
    # request_and_print("url-which", track_url)

@spotify_plus.command()
def song_which(song_name: str):
    pass

def request_and_print(command, arguments):
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