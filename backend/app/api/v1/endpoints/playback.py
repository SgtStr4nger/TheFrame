from fastapi import APIRouter, Depends
from app.services.spotify_client import SpotifyClient
from app.models.schemas import PlaybackInfoResponse

router = APIRouter()

@router.get("/playback")
async def get_playback_info(spotify: SpotifyClient = Depends()):
    return {
        "track": spotify.playback_state.get_state()['track'],
        "progress": spotify.playback_state.get_state()['progress'],
        "is_playing": spotify.playback_state.get_state()['is_playing']
    }
