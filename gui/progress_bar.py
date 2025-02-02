import tkinter as tk
import time


class ProgressBar:
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, highlightthickness=0, height=10)  # Transparent
        self.canvas.place(relx=0.5, rely=0.9, anchor=tk.CENTER, width=700)
        self.current_progress = 0
        self.target_progress = 0
        self.previous_progress = 0
        self.animation_running = False

    def _draw_progress(self, percentage):
        self.canvas.delete('all')
        width = self.canvas.winfo_width()
        progress_width = (percentage / 100) * width

        # Darker progress color (#404040)
        self.canvas.create_rectangle(
            0, 0, progress_width, 10,
            fill='#444444',  # Darker gray
            outline=''
        )



    def update_progress(self, percentage, force=False):
        """Update progress with pause handling"""
        self.previous_progress = self.current_progress  # Store previous state
        self.target_progress = percentage
        if not self.animation_running:
            self.animation_running = True
            self._animate()

    def _animate(self):
        if not self.animation_running:
            return

        # Start from previous progress instead of zero
        step = (self.target_progress - self.previous_progress) * 0.3
        self.current_progress = self.previous_progress + step

        if abs(self.target_progress - self.current_progress) < 0.5:
            self.current_progress = self.target_progress
            self.previous_progress = self.current_progress
            self.animation_running = False

        self._draw_progress(self.current_progress)

        if self.animation_running:
            self.canvas.after(16, self._animate)

    def start_animation(self, duration_ms):
        self.duration = duration_ms / 1000  # Convert to seconds
        self.start_time = time.time()
        self.animation_running = True
        self._animate()

    def pause_animation(self):
        self.animation_running = False

    def reset_animation(self):
        """Instant reset for new tracks"""
        self.current_progress = 0
        self.target_progress = 0
        self.animation_running = False
        self._draw_progress(0)  # Force immediate visual update


    def resize(self, window_width):
        """Handle window resizing"""
        self.canvas.config(width=window_width * 0.8)
        self._draw_progress(self.current_progress)

