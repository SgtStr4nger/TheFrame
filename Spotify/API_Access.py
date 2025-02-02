import spotipy
from PIL import Image
import requests

from spotipy.oauth2 import SpotifyOAuth

def SetupSpotifyAPI():
    ClientID = "-"
    ClientSecret = "-"
    URL = "http://localhost:3000"
    scope = "user-read-currently-playing"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=ClientID,
                                                   client_secret=ClientSecret,
                                                   redirect_uri=URL,
                                                   scope=scope))
    return sp



def CurrentlyPlaying(sp):
    CurrentSongInfo = sp.current_user_playing_track()

    CurrentSong = {
        "cover_url": CurrentSongInfo["item"]["album"]["images"][0]["url"],
        "title": CurrentSongInfo["item"]["name"],
        "artist": CurrentSongInfo["item"]["album"]["artists"][0]["name"],
    }

    return CurrentSong


def GetCover(sp):
    cover_file = "cover.jpg"
    cover = Image.open(requests.get(CurrentlyPlaying(sp)["cover_url"], stream=True).raw)
    cover.save(cover_file)

    return cover_file

