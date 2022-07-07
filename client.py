import sys
sys.dont_write_bytecode = True
from difflib import get_close_matches

import typer

from globals import *
from utils.library_loader import *


spotify_plus = typer.Typer()

# Fetches the secondary-account playlists a given song link is contained within
@spotify_plus.command()
def url_which(track_url: str):
    pass

@spotify_plus.command()
def song_which(song_name: str):
    pass


if __name__ == "__main__":
    spotify_plus()