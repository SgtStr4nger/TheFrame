import time
from threading import Lock

class PlaybackState:
    def __init__(self):
        self._lock = Lock()
        self._state = {
            'track': None,
            'progress': 0.0,
            'is_playing': False
        }

    def update_state(self, raw_data):
        """Thread-safe state update"""
        with self._lock:
            # Existing state update logic from playback_state.py
            # Convert raw API data to normalized format
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

    def current_track_info(self):
        with self._lock:
            return self._state['track']

    def get_current_progress(self):
        with self._lock:
            return self._state['progress']
