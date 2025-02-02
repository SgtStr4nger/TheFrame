import tkinter as tk
from PIL import Image, ImageTk, ImageOps, ImageFilter
import requests
from io import BytesIO
from .progress_bar import ProgressBar


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("TheFrame")
        self.root.geometry("1000x1000")
        self.root.configure(bg='#000000')

        # Create main canvas with proper expansion
        self.main_canvas = tk.Canvas(self.root, bg='#000000', highlightthickness=0)
        self.main_canvas.pack(fill=tk.BOTH, expand=True)

        # Initialize elements with proper centering
        self.current_url = None
        self.current_album_art = None
        self.background_image = None

        self._create_ui_elements()
        self._setup_bindings()

        # Force initial positioning
        self.root.update_idletasks()
        self._position_elements()

    def _create_ui_elements(self):
        """Create all UI elements with center alignment"""
        # Background image (centered)
        self.background_image_id = self.main_canvas.create_image(
            0, 0, anchor=tk.NW, tags='background'
        )

        # Album Art (centered)
        self.album_art_id = self.main_canvas.create_image(
            0, 0, anchor=tk.CENTER, tags='album_art'
        )

        # Text Elements (centered)
        self.title_id = self.main_canvas.create_text(
            0, 0,
            font=('Arial', 32, 'bold'),
            fill='#ffffff',
            anchor=tk.CENTER,
            tags='text'
        )
        self.artist_id = self.main_canvas.create_text(
            0, 0,
            font=('Arial', 24),
            fill='#cccccc',
            anchor=tk.CENTER,
            tags='text'
        )

        # Progress Bar (centered at bottom)
        self.progress_bar = ProgressBar(self.main_canvas)

    def _setup_bindings(self):
        self.root.bind('<Configure>', self._handle_resize)

    def _position_elements(self):
        """Center all elements based on current window size"""
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Center album art
        self.main_canvas.coords(self.album_art_id, width / 2, height * 0.4)

        # Center text
        self.main_canvas.coords(self.title_id, width / 2, height * 0.75)
        self.main_canvas.coords(self.artist_id, width / 2, height * 0.8)

        # Update progress bar position
        self.progress_bar.resize(width)

    def update_interface(self, track_info):
        """Update all visual elements"""
        self._update_background(track_info['album_art'])
        self._update_album_art(track_info['album_art'])
        self._update_text(track_info)
        self.progress_bar.update_progress(
            (track_info['progress_ms'] / track_info['duration_ms']) * 100
        )

    def _update_background(self, image_url):
        try:
            response = requests.get(image_url, timeout=5)
            img = Image.open(BytesIO(response.content))

            # Get current window size
            width = self.root.winfo_width()
            height = self.root.winfo_height()

            # Process and center background
            img = ImageOps.fit(img.convert('RGB'), (width, height))
            blurred = img.filter(ImageFilter.GaussianBlur(radius=25))
            self.background_image = ImageTk.PhotoImage(blurred)

            self.main_canvas.itemconfig(self.background_image_id, image=self.background_image)
            self.main_canvas.tag_lower('background')

        except Exception as e:
            print(f"Background error: {str(e)}")

    def _update_album_art(self, image_url):
        try:
            response = requests.get(image_url, timeout=5)
            img = Image.open(BytesIO(response.content))
            img = ImageOps.contain(img.convert("RGBA"), (600, 600))

            self.current_album_art = ImageTk.PhotoImage(img)
            self.main_canvas.itemconfig(self.album_art_id, image=self.current_album_art)
            self.main_canvas.tag_raise('album_art')

            # Center album art after update
            self._position_elements()

        except Exception as e:
            print(f"Album art error: {str(e)}")

    def _update_text(self, track_info):
        self.main_canvas.itemconfig(self.title_id, text=track_info['title'])
        self.main_canvas.itemconfig(self.artist_id, text=track_info['artist'])
        self.main_canvas.tag_raise('text')

    def _handle_resize(self, event):
        """Handle window resizing"""
        if event.widget == self.root:
            self._position_elements()
            if self.current_url:
                self._update_background(self.current_url)

    def update_progress(self, percentage):
        self.progress_bar.update_progress(percentage)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
