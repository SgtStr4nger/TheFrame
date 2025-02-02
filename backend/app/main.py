import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.services.spotify_client import SpotifyClient

from app.core.config import settings
print("Spotify Client ID:", settings.SPOTIPY_CLIENT_ID)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler with modern FastAPI pattern"""
    # Startup logic
    spotify_client = SpotifyClient()
    app.state.spotify_client = spotify_client
    spotify_client.start_polling()

    yield  # Application runs here

    # Shutdown logic
    spotify_client.stop_polling()


app = FastAPI(
    title="Spotify Player Backend",
    lifespan=lifespan
)

@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}