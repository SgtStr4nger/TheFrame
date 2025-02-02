import os
import threading
import time
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from backend.app.core.playback_state import PlaybackState
from backend.app.services.websocket_manager import websocket_manager
from backend.app.core.config import settings
from dotenv import load_dotenv

class SpotifyClient:
    def __init__(self):
        self.playback_state = PlaybackState()
        self.sp = self._create_client()
        self._polling_thread = None
        self._running = False
        load_dotenv()

    def _create_client(self):
        return Spotify(auth_manager=SpotifyOAuth(
            scope='user-read-currently-playing user-read-playback-state',
            client_id=settings.SPOTIPY_CLIENT_ID,        # Changed from os.getenv
            client_secret=settings.SPOTIPY_CLIENT_SECRET, # Changed from os.getenv
            redirect_uri=settings.SPOTIPY_REDIRECT_URI,
            cache_path='.cache'
        ))

    def start_polling(self):
        if not self._running:
            self._running = True
            self._polling_thread = threading.Thread(target=self._poll_loop)
            self._polling_thread.start()

    def _poll_loop(self):
        while self._running:
            try:
                data = self.sp.current_playback()
                if data and data.get('is_playing'):
                    self.playback_state.update_state(data)
                    websocket_manager.broadcast({
                        "type": "playback_update",
                        "data": self.playback_state.get_state()
                    })
            except Exception as e:
                print(f"Polling error: {str(e)}")
            time.sleep(2)

    def stop_polling(self):
        self._running = False
        if self._polling_thread:
            self._polling_thread.join()
