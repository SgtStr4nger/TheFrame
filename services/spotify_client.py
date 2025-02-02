import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import time
import threading
from dotenv import load_dotenv



class SpotifyClient:
    def __init__(self, callback):
        # Store auth_manager as instance variable
        load_dotenv()
        self.auth_manager = SpotifyOAuth(
            scope='user-read-currently-playing user-read-playback-state',
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
            cache_path='.cache'
        )

        # Initialize Spotipy with the auth_manager
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)
        self.callback = callback
        self.running = True
        self.thread = threading.Thread(target=self._poll)
        self.thread.start()


    def _refresh_token(self):
        try:
            # Get cached token and validate existence
            token_info = self.auth_manager.get_cached_token()

            if not token_info:
                print("No cached token found. Re-authenticate!")
                return None

            # Validate token structure
            if 'refresh_token' not in token_info:
                print("Token missing refresh_token. Re-authenticate!")
                return None

            # Refresh if expired
            if self.auth_manager.is_token_expired(token_info):
                new_token = self.auth_manager.refresh_access_token(token_info['refresh_token'])
                if not new_token:
                    raise ValueError("Token refresh failed: Empty response")
                return new_token

            return token_info

        except Exception as e:
            print(f"Token refresh error: {str(e)}")
            return None

    def _poll(self):
        while self.running:
            try:
                token_info = self._refresh_token()

                if not token_info:
                    print("Authentication required. Restart the app!")
                    time.sleep(5)
                    continue

                # Validate access token
                if 'access_token' not in token_info:
                    print("Invalid token structure")
                    continue

                sp = spotipy.Spotify(auth=token_info['access_token'])
                data = sp.current_playback()

                if data and data.get('is_playing'):
                    self.callback('update', data)
                time.sleep(2)

            except spotipy.SpotifyException as e:
                if e.http_status == 401:
                    print("Token expired. Forcing re-authentication...")
                    os.remove(".cache")  # Clear invalid token
            except Exception as e:
                print(f"Polling error: {str(e)}")
                time.sleep(5)