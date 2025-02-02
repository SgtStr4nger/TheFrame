from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SPOTIPY_CLIENT_ID: str
    SPOTIPY_CLIENT_SECRET: str
    SPOTIPY_REDIRECT_URI: str
    SPOTIPY_SCOPE: str = 'user-read-currently-playing user-read-playback-state'

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'  # Allow extra fields
    )

settings = Settings()