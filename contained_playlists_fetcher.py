# Playlist fetcher for checking what playlists a song-link I want to add is within

import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('SPOTIPY_CLIENT_ID_CONTAINED_PLAYLISTS_FETCHER'), client_secret=os.getenv('SPOTIPY_CLIENT_SECRET_CONTAINED_PLAYLISTS_FETCHER'))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

library_account = os.getenv('SPOTIFY_PLUS_SECONDARY_ACCOUNT_USER_ID')

playlists = sp.user_playlists(library_account)

while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" %
            (i + 1 + playlists['offset'], playlist['uri'], playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None