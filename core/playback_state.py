import time


class PlaybackState:
    def __init__(self):
        self.start_time = None
        self.duration = 0
        self.last_progress = 0
        self.playing = False
        self.current_track_id = None
        self.pause_time = None  # Track when playback was paused

    def update_state(self, track_info):
        """Update playback state from Spotify API response"""
        if not track_info or 'item' not in track_info:
            return

        new_track_id = track_info['item']['id']
        new_playing_state = track_info['is_playing']

        # Handle play/pause transitions
        if self.playing != new_playing_state:
            if new_playing_state:
                # Resuming playback
                if self.pause_time:
                    pause_duration = time.time() - self.pause_time
                    self.start_time += pause_duration
                    self.pause_time = None
            else:
                # Pausing playback
                self.pause_time = time.time()
                self.last_progress = self.get_current_progress()

        # Handle track changes
        if new_track_id != self.current_track_id:
            self._handle_new_track(track_info)

        self.playing = new_playing_state
        self.duration = track_info['item']['duration_ms'] / 1000  # Convert to seconds

        # Initialize start time for new playback
        if self.playing and not self.start_time:
            self.start_time = time.time() - (track_info['progress_ms'] / 1000)

    def _handle_new_track(self, track_info):
        """Reset state for new track"""
        self.current_track_id = track_info['item']['id']
        self.start_time = time.time() - (track_info['progress_ms'] / 1000)
        self.last_progress = 0
        self.pause_time = None

    def get_current_progress(self):
        """Calculate current progress with smooth updates"""
        if not self.playing:
            return self.last_progress

        elapsed = time.time() - self.start_time
        self.last_progress = min(elapsed, self.duration)
        return self.last_progress
