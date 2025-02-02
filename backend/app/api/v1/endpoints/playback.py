from fastapi import APIRouter, Depends
from backend.app.services.spotify_client import SpotifyClient
from backend.app.models.schemas import PlaybackInfoResponse

router = APIRouter()

@router.get("/playback", response_model=PlaybackInfoResponse)
async def get_playback_info(spotify: SpotifyClient = Depends()):
    """Get current playback information"""
    return {
        "track": spotify.playback_state.current_track_info(),
        "progress": spotify.playback_state.get_current_progress(),
        "is_playing": spotify.playback_state.is_playing
    }
