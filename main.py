import tkinter as tk
from gui.main_window import MainWindow
from core.playback_state import PlaybackState
from services.spotify_client import SpotifyClient
from dotenv import load_dotenv

load_dotenv()

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = MainWindow(self.root)
        self.playback_state = PlaybackState()
        self.spotify_client = SpotifyClient(self.handle_update)
        self.root.after(16, self.update_progress)

    def handle_update(self, event_type, data):
        """Handle updates from Spotify client"""
        try:
            if data and data.get('item'):
                # Fixed: Added missing closing brace for track_info dictionary
                track_info = {
                    'title': data['item']['name'],
                    'artist': ', '.join([a['name'] for a in data['item']['artists']]),
                    'album_art': data['item']['album']['images'][0]['url'],
                    'progress_ms': data['progress_ms'],
                    'duration_ms': data['item']['duration_ms'],
                    'is_playing': data['is_playing']
                }
                self.gui.update_interface(track_info)
        except Exception as e:
            print(f"Error in handle_update: {str(e)}")
            import traceback
            traceback.print_exc()

    def update_progress(self):
        """Update progress bar at 60 FPS when playing"""
        if self.playback_state.playing:
            progress = self.playback_state.get_current_progress()
            if self.playback_state.duration > 0:
                self.gui.update_progress(
                    (progress / self.playback_state.duration) * 100
                )
            # Fixed: Moved after() call outside conditional
            self.root.after(16, self.update_progress)
        else:
            self.root.after(16, self.update_progress)

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()
        self.spotify_client.stop()

if __name__ == "__main__":
    app = Application()
    app.run()
