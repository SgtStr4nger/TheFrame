import time


class PlaybackState:
    """Track and manage playback state information"""

    def __init__(self):
        self.start_time = None  # Timestamp when playback started
        self.duration = 0  # Track duration in seconds
        self.last_progress = 0  # Last known playback position
        self.playing = False  # Current play/pause state
        self.current_track_id = None  # Current track identifier
        self.pause_time = None  # Timestamp when paused

    def update_state(self, track_info):
        """Handle seek events and proper pause state"""
        if not track_info or 'item' not in track_info:
            return

        # Handle seek events
        if self.current_track_id == track_info['item']['id'] and \
                abs(track_info['progress_ms'] - self.last_progress * 1000) > 1000:
            self._handle_seek(track_info['progress_ms'])

        new_track_id = track_info['item']['id']
        new_playing_state = track_info['is_playing']

        # Handle play/pause state transitions
        if self.playing != new_playing_state:
            if new_playing_state:
                self._handle_play()
            else:
                self._handle_pause()

        # Handle track changes
        if new_track_id != self.current_track_id:
            self._handle_new_track(track_info)

        # Update duration in seconds (convert from ms)
        self.duration = track_info['item']['duration_ms'] / 1000

        # Initialize start time for new playback
        if self.playing and not self.start_time:
            self.start_time = time.time() - (track_info['progress_ms'] / 1000)

    def get_current_progress(self):
        if self.playing:
            # Calculate elapsed time since playback started
            elapsed = time.time() - self.start_time
            # Never return progress exceeding track duration
            self.last_progress = min(elapsed, self.duration)
        return self.last_progress


    def _handle_play(self):
        """Resume playback after pause"""
        if self.pause_time:
            pause_duration = time.time() - self.pause_time
            self.start_time += pause_duration
            self.pause_time = None

    def _handle_pause(self):
        """Pause playback and store current position"""
        self.pause_time = time.time()
        self.last_progress = self.get_current_progress()

    def _handle_seek(self, new_progress_ms):
        """Update timing for seek operations"""
        self.last_progress = new_progress_ms / 1000
        if self.playing:
            self.start_time = time.time() - self.last_progress


    def _handle_new_track(self, track_info):
        """Reset state for new track"""
        self.current_track_id = track_info['item']['id']
        # Set initial progress from API data
        self.last_progress = track_info['progress_ms'] / 1000
        # Calculate accurate start time considering current progress
        self.start_time = time.time() - self.last_progress