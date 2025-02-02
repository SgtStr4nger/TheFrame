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
                track_info = {
                    'title': data['item']['name'],
                    'artist': ', '.join([a['name'] for a in data['item']['artists']]),
                    'album_art': data['item']['album']['images'][0]['url']
                }
                self.gui.update_interface(track_info)

        except Exception as e:
            print(f"Error in handle_update: {str(e)}")
            import traceback
            traceback.print_exc()

    def update_progress(self):
        if self.playback_state.playing:
            progress = self.playback_state.get_current_progress()
            if self.playback_state.duration > 0:
                self.gui.update_progress(
                    (progress / self.playback_state.duration) * 100
                )  # Fixed missing parenthesis
            self.root.after(16, self.update_progress)

    def run(self):
        self.root.mainloop()
        self.spotify_client.stop()

if __name__ == "__main__":
    app = Application()
    app.run()