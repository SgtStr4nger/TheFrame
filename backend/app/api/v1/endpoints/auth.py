from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from spotipy.oauth2 import SpotifyOAuth
import os

router = APIRouter()


@router.get("/login")
async def login():
    auth_manager = SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope='user-read-currently-playing user-read-playback-state'
    )
    auth_url = auth_manager.get_authorize_url()
    return RedirectResponse(auth_url)


@router.get("/callback")
async def callback(code: str = None, error: str = None):
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authorization failed: {error}"
        )

    auth_manager = SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI')
    )

    try:
        token_info = auth_manager.get_access_token(code)
        return {"status": "authenticated"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )
