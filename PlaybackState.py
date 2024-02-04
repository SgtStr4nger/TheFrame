import spotipy


def get_remaining_time(sp):

    try:
        # Get current user's playback information
        current_track = sp.current_user_playing_track()

        # Check if a track is currently playing
        if current_track is not None and current_track.get('is_playing', False):
            duration_ms = current_track['item']['duration_ms']
            progress_ms = current_track['progress_ms']
            return duration_ms-progress_ms


        else:
            print("No track is currently playing.")

    except spotipy.SpotifyException as e:
        print(f"Error: {e}")
