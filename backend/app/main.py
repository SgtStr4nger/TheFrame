from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.spotify_client import SpotifyClient
from app.core.config import settings
from app.api.v1.endpoints import auth, playback, websocket

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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with proper prefixes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(playback.router, prefix="/api/v1", tags=["playback"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])
@app.get("/")
async def root():
    """Root endpoint to verify API is running"""
    return {"status": "online", "service": "Spotify Player API"}

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }