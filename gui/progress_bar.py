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
    ]  # Fixed missing closing bracket
    return self.create_polygon(points, **kwargs, smooth=True)


tk.Canvas.create_rounded_rectangle = create_rounded_rectangle


class ProgressBar:
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, bg='#000000', highlightthickness=0, height=25)
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
        self._draw_progress(progress)

        if progress < 100:
            self.canvas.after(16, self._animate)

    def _draw_progress(self, percentage):
        self.canvas.delete('all')
        width = self.canvas.winfo_width()
        pos = (percentage / 100) * width

        # Draw track background
        self.canvas.create_rounded_rectangle(
            0, 5, width, 15,
            radius=10, fill='#404040', outline='#606060'
        )  # Fixed missing parenthesis

        # Draw progress indicator
        self.canvas.create_oval(
            pos - 10, 0,
            pos + 10, 20,
            fill='#ffffff', outline='#a0a0a0'
        )  # Fixed missing parenthesis

    def stop_animation(self):
        self.animation_running = False

    def update_progress(self, percentage):
        self._draw_progress(percentage)

    def resize(self, width):
        self.canvas.config(width=width * 0.8)
        self._draw_progress((self.current_progress / 100) * width)
