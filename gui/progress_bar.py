import tkinter as tk
import time


def create_rounded_rectangle(self, x1, y1, x2, y2, radius=55, **kwargs):
    """Custom rounded rectangle implementation"""
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1, y1
    ]
    return self.create_polygon(points, **kwargs, smooth=True)


tk.Canvas.create_rounded_rectangle = create_rounded_rectangle


class ProgressBar:
    def __init__(self, parent):
        # Make canvas transparent
        self.canvas = tk.Canvas(parent, highlightthickness=0, height=25)
        self.canvas.place(relx=0.5, rely=0.9, anchor=tk.CENTER, width=700)
        self.current_progress = 0
        self.animation_running = False

    def start_animation(self, duration_ms, initial_progress=0):
        self.duration = duration_ms / 1000
        self.start_time = time.time() - (initial_progress / 1000)
        self.animation_running = True
        self._animate()

    def _animate(self):
        if not self.animation_running:
            return

        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.duration, 1.0) * 100

        # Update even if small change for smooth animation
        self._draw_progress(progress)
        self.current_progress = progress

        if progress < 100:
            self.canvas.after(16, self._animate)  # Restore 60 FPS

    def _draw_progress(self, percentage):
        self.canvas.delete('all')
        width = self.canvas.winfo_width()
        pos = (percentage / 100) * width

        # Draw track background (completely transparent)
        self.canvas.create_rounded_rectangle(
            0, 5, width, 15,
            radius=10,
            fill='',  # Empty string for transparent fill
            outline='#ffffff'  # White outline
        )

        # Draw progress indicator
        self.canvas.create_oval(
            pos - 10, 0,
            pos + 10, 20,
            fill='#cccccc',  # Light grey fill
            outline='#ffffff'  # White outline
        )

    def stop_animation(self):
        self.animation_running = False

    def update_progress(self, percentage):
        """Update progress directly without animation"""
        self._draw_progress(percentage)
        self.current_progress = percentage

    def resize(self, window_width):
        """Handle window resizing"""
        self.canvas.config(width=window_width * 0.8)
        self._draw_progress(self.current_progress)