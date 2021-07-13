import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import os
import json
from dotenv import load_dotenv
import random

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                                               client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                                               redirect_uri='http://localhost/',
                                               scope="user-library-read user-read-recently-played",
                                               cache_path="../.cache"))


# sp = spotipy.Spotify(auth_manager=SpotifyOAuth())

# albums = sp.current_user_saved_albums(limit=50, offset=250)
recently_played = sp.current_user_recently_played(limit=50)

# for idx, item in enumerate(recently_played['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])

# for item in albums['items']:
#     tracks = item['album']['tracks']
#     for idx, track in enumerate(tracks['items']):
#         print(idx, track['artists'][0]['name'], " – ", track['name'])


def get_random_recently_played():
    """returns a random song from my last 50 played songs"""
    i = random.randint(0, 49)
    track = recently_played['items'][i]['track']
    link = "https://open.spotify.com/track/" + track['uri'].split(":")[-1]
    out = track['artists'][0]['name'] + " – " + track['name'] + '\n' + link
    return out
