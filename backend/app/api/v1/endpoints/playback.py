from fastapi import APIRouter, Depends, Request
from app.services.spotify_client import SpotifyClient
from app.models.schemas import PlaybackInfoResponse

router = APIRouter()

@router.get("/playback")
async def get_playback_info(request: Request):
    spotify_client = request.app.state.spotify_client
    return spotify_client.playback_state.get_state()
