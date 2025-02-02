import time
from threading import Lock

class PlaybackState:
    def __init__(self, spotify_client=None):
        self._lock = Lock()
        self._state = {
            'track': None,
            'progress': 0.0,
            'is_playing': False
        }
        self.sp = spotify_client

    def get_state(self):
        """Get current state with validation"""
        with self._lock:
            if self._state['track'] is None and self.sp:
                try:
                    data = self.sp.current_playback()
                    if data:
                        self.update_state(data)
                except Exception as e:
                    print(f"Error fetching state: {str(e)}")
            return self._state.copy()

    def update_state(self, raw_data):
        """Thread-safe state update"""
        with self._lock:
            if raw_data and 'item' in raw_data:
                try:
                    self._state = {
                        'track': {
                            'title': raw_data['item']['name'],
                            'artist': ', '.join(a['name'] for a in raw_data['item']['artists']),
                            'album_art': raw_data['item']['album']['images'][0]['url'],
                            'duration': raw_data['item']['duration_ms'] / 1000
                        },
                        'progress': raw_data['progress_ms'] / 1000,
                        'is_playing': raw_data['is_playing']
                    }
                    print(f"State updated successfully: {self._state}")
                except Exception as e:
                    print(f"Error updating state: {str(e)}")
                    print(f"Raw data: {raw_data}")

    def current_track_info(self):
        with self._lock:
            return self._state['track']

    def get_current_progress(self):
        with self._lock:
            return self._state['progress']
