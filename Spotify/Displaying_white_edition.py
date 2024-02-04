from Spotify.API_Access import CurrentlyPlaying, SetupSpotifyAPI, GetCover

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QWidget, QGraphicsBlurEffect, \
    QGraphicsScene, QGraphicsPixmapItem, QGraphicsView
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, QTimer

from PlaybackState import get_remaining_time


class BackgroundOverlay(QGraphicsView):
    def __init__(self, parent, image_path, blur_radius, overlay_alpha):
        super().__init__(parent)
        self.image_path = image_path
        self.blur_radius = blur_radius
        self.overlay_alpha = overlay_alpha
        self.init_ui()

    def init_ui(self):
        scene = QGraphicsScene(self)
        self.setScene(scene)

        # Load the cover image without scaling
        cover_pixmap = QPixmap(self.image_path)

        # Blur effect with specified radius
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(self.blur_radius)

        # Darken the background with a semi-transparent overlay
        overlay_color = QColor(0, 0, 0, self.overlay_alpha)
        overlay_pixmap = QPixmap(self.size())
        overlay_pixmap.fill(overlay_color)

        # Create a label for the background image
        background_label = QGraphicsPixmapItem(cover_pixmap)
        background_label.setGraphicsEffect(blur)
        scene.addItem(background_label)

        # Create a label for the overlay
        overlay_label = QGraphicsPixmapItem(overlay_pixmap)
        scene.addItem(overlay_label)


class TheFrame_Spotify(QWidget):
    def __init__(self):
        super().__init__()

        self.sp = SetupSpotifyAPI()

        # Set up the window
        self.setWindowTitle("The Frame")
        self.setGeometry(100, 100, 1920, 1080)

        # Set the background image to cover.jpg with a stronger blur effect
        self.set_background_image("cover.jpg", blur_radius=1000, overlay_alpha=1)

        # Create a grid layout with 4 rows and 3 columns
        grid_layout = QGridLayout(self)

        # Add widgets to the grid
        for row in range(6):
            for col in range(3):
                grid_layout.addWidget(QLabel(""), row, col)

        # Set the width of the second column to a fixed width of 640
        grid_layout.setColumnMinimumWidth(1, 640)
        grid_layout.setColumnStretch(1, 0)  # Disable stretching for the second column

        # Set Title
        self.Set_title(grid_layout)

        # Set Artist
        self.Set_artist(grid_layout)

        # Insert Cover in Row 2, Column 2
        self.Set_cover(grid_layout)

        self.set_update_timer()

        self.setLayout(grid_layout)

    def set_update_timer(self):
        # Set up a timer for periodic updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_information)
        self.timer.start(get_remaining_time(self.sp))

    def Set_cover(self, grid_layout):
        self.image_label = QLabel(self)
        self.image_pixmap = QPixmap(GetCover(self.sp))  # Replace with your image file path
        self.image_label.setPixmap(self.image_pixmap)  # Adjust width as needed
        self.image_label.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(self.image_label, 1, 1, 1, 1)  # Span one row and one column

    def Set_artist(self, grid_layout):
        self.title_label_artist = QLabel(self)
        self.title_label_artist.setStyleSheet("color: #3b3b3b; font-size: 14px;")
        self.title_label_artist.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.title_label_artist.setText(CurrentlyPlaying(self.sp)["artist"])
        grid_layout.addWidget(self.title_label_artist, 3, 1)

    def Set_title(self, grid_layout):
        self.title_label_title = QLabel(self)
        self.title_label_title.setStyleSheet("color: #222222; font-size: 16px; font-weight: bold;")
        self.title_label_title.setAlignment(Qt.AlignCenter)
        self.title_label_title.setText(CurrentlyPlaying(self.sp)["title"])
        grid_layout.addWidget(self.title_label_title, 2, 1)

    def update_information(self):
        # Update the information here
        self.title_label_title.setText(CurrentlyPlaying(self.sp)["title"])
        self.title_label_artist.setText(CurrentlyPlaying(self.sp)["artist"])
        self.image_pixmap = QPixmap(GetCover(self.sp))  # Replace with your image file path
        self.image_label.setPixmap(self.image_pixmap)
        self.set_update_timer()

    def set_background_image(self, image_path, blur_radius, overlay_alpha):
        overlay = BackgroundOverlay(self, image_path, blur_radius, overlay_alpha)
        overlay.setGeometry(0, 0, self.width(), self.height())
        overlay.show()





def main():
    app = QApplication(sys.argv)
    window = TheFrame_Spotify()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
