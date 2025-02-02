import tkinter as tk
from PIL import Image, ImageTk, ImageOps, ImageFilter
import requests
from io import BytesIO
from .progress_bar import ProgressBar


class MainWindow:
    """Main application window handling UI components"""

    def __init__(self, root):
        self.root = root
        self.root.title("TheFrame")
        self.root.geometry("1000x1000")
        self.root.configure(bg='#000000')

        # Image references to prevent garbage collection
        self.background_image = None
        self.album_art_image = None

        # Main canvas setup
        self.main_canvas = tk.Canvas(self.root, bg='#000000', highlightthickness=0)
        self.main_canvas.pack(fill=tk.BOTH, expand=True)

        # UI elements initialization
        self._create_ui_elements()
        self._setup_bindings()

        # Force initial layout calculation
        self.root.update_idletasks()
        self._position_elements()

    def _create_ui_elements(self):
        """Initialize all UI components"""
        # Background image (centered)
        self.background_image_id = self.main_canvas.create_image(
            0, 0, anchor=tk.NW, tags='background'
        )

        # Album art display
        self.album_art_id = self.main_canvas.create_image(
            0, 0, anchor=tk.CENTER, tags='album_art'
        )

        # Text elements
        self.title_id = self.main_canvas.create_text(
            0, 0,
            text="Loading...",
            font=('Arial', 32, 'bold'),
            fill='#ffffff',
            anchor=tk.CENTER,
            tags='text'
        )

        self.artist_id = self.main_canvas.create_text(
            0, 0,
            text="Waiting for track...",
            font=('Arial', 24),
            fill='#cccccc',
            anchor=tk.CENTER,
            tags='text'
        )

        # Progress bar
        self.progress_bar = ProgressBar(self.main_canvas)

    def _setup_bindings(self):
        """Set up event handlers"""
        self.root.bind('<Configure>', self._handle_resize)

    def _position_elements(self):
        """Position elements based on current window size"""
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Position album art at 40% window height
        self.main_canvas.coords(self.album_art_id, width / 2, height * 0.4)

        # Position text elements
        self.main_canvas.coords(self.title_id, width / 2, height * 0.75)
        self.main_canvas.coords(self.artist_id, width / 2, height * 0.8)

        # Update progress bar width
        self.progress_bar.resize(width)

    def update_interface(self, track_info):
        """Update all UI elements with new track info"""
        self._update_background(track_info['album_art'])
        self._update_album_art(track_info['album_art'])
        self._update_text(track_info)
        self._update_progress(track_info)

    def _update_background(self, image_url):
        """Update blurred background image"""
        try:
            response = requests.get(image_url, timeout=5)
            response.raise_for_status()

            img = Image.open(BytesIO(response.content))
            img = ImageOps.fit(img.convert('RGB'),
                               (self.root.winfo_width(), self.root.winfo_height()))
            blurred = img.filter(ImageFilter.GaussianBlur(radius=25))

            # Maintain reference to prevent garbage collection
            self.background_image = ImageTk.PhotoImage(blurred)
            self.main_canvas.itemconfig(self.background_image_id,
                                        image=self.background_image)
            self.main_canvas.tag_lower('background')

        except Exception as e:
            print(f"Background error: {str(e)}")
            self.main_canvas.configure(bg='#000000')

    def _update_album_art(self, image_url):
        """Update album artwork display"""
        try:
            response = requests.get(image_url, timeout=5)
            response.raise_for_status()

            img = Image.open(BytesIO(response.content))
            img = ImageOps.contain(img.convert("RGBA"), (600, 600))

            # Maintain reference to prevent garbage collection
            self.album_art_image = ImageTk.PhotoImage(img)
            self.main_canvas.itemconfig(self.album_art_id,
                                        image=self.album_art_image)
            self.main_canvas.tag_raise('album_art')

        except Exception as e:
            print(f"Album art error: {str(e)}")
            self.main_canvas.itemconfig(self.title_id, text="Artwork unavailable")

    def _update_text(self, track_info):
        """Update track metadata display"""
        self.main_canvas.itemconfig(self.title_id, text=track_info['title'])
        self.main_canvas.itemconfig(self.artist_id, text=track_info['artist'])
        self.main_canvas.tag_raise('text')

    def _update_progress(self, track_info):
        """Update progress bar position"""
        if track_info['duration_ms'] > 0:  # Prevent division by zero
            progress = (track_info['progress_ms'] / track_info['duration_ms']) * 100
            self.progress_bar.update_progress(progress)

    def _handle_resize(self, event):
        """Handle window resize events"""
        if event.widget == self.root:
            self._position_elements()
            if hasattr(self, 'current_url'):
                self._update_background(self.current_url)

    def update_progress(self, percentage):
        """Update progress bar percentage (0-100)"""
        self.progress_bar.update_progress(percentage)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
