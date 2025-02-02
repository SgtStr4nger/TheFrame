from pydantic import BaseModel

class TrackInfo(BaseModel):
    title: str
    artist: str
    album_art: str
    duration: float

class PlaybackInfoResponse(BaseModel):
    track: TrackInfo
    progress: float
    is_playing: bool
