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

        @property
        def is_playing(self):
            """Get current playing state"""
            with self._lock:
                return self._state['is_playing']

    def get_state(self):
        """Return the complete state object"""
        with self._lock:
            print("Getting state:", self._state)
            return {
                'track': self._state['track'],
                'progress': self._state['progress'],
                'is_playing': self._state['is_playing']
            }

    def update_state(self, raw_data):
        print("Before update:", self._state)
        with self._lock:
            if raw_data and 'item' in raw_data:
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
                print("After update:", self._state)
            else:
                print("Received empty or invalid playback data")

    def current_track_info(self):
        with self._lock:
            return self._state['track']

    def get_current_progress(self):
        with self._lock:
            return self._state['progress']
