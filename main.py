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
        try:
            if data and data.get('item'):
                current_track_id = data['item']['id']

                # Only update UI elements on track change
                if current_track_id != self.playback_state.current_track_id:
                    track_info = {
                        'title': data['item']['name'],
                        'artist': ', '.join([a['name'] for a in data['item']['artists']]),
                        'album_art': data['item']['album']['images'][0]['url'],
                        'progress_ms': data['progress_ms'],
                        'duration_ms': data['item']['duration_ms']
                    }
                    self.gui.update_interface(track_info)

                # Always update playback state
                self.playback_state.update_state(data)

        except Exception as e:
            print(f"Update error: {str(e)}")
            import traceback
            traceback.print_exc()

    def update_progress(self):
        """Update only progress bar at 60 FPS"""
        try:
            progress = self.playback_state.get_current_progress()
            if self.playback_state.duration > 0:
                percentage = (progress / self.playback_state.duration) * 100
                self.gui.progress_bar.update_progress(percentage)
        finally:
            self.root.after(16, self.update_progress)

    def run(self):
        self.root.mainloop()
        self.spotify_client.stop()


if __name__ == "__main__":
    app = Application()
    app.run()
