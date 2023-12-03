import spotipy
from PIL import Image
import requests

from spotipy.oauth2 import SpotifyOAuth

ClientID = "eced503c8a0d459598f1740a7dcae605"
ClientSecret = "b727777a758747c0bd64daaae85e4dde"
URL = "http://localhost:3000"
scope = "user-read-currently-playing"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope=scope, client_id=ClientID, client_secret=ClientSecret, redirect_uri=URL))


def CurrentlyPlaying():
    CurrentSongInfo = sp.current_user_playing_track()

    CurrentSong = {
        "cover_url": CurrentSongInfo["item"]["album"]["images"][0]["url"],
        "titel": CurrentSongInfo["item"]["name"],
        "artist": CurrentSongInfo["item"]["album"]["artists"][0]["name"],
    }

    return CurrentSong


def GetCover():
    cover_file = "cover.jpg"
    cover = Image.open(requests.get(CurrentlyPlaying()["cover_url"], stream=True).raw)
    cover.save(cover_file)

    return cover_file

GetCover()