from API_Access import CurrentlyPlaying, SetupSpotifyAPI, GetCover

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QWidget, QGraphicsBlurEffect, \
    QGraphicsScene, QGraphicsPixmapItem, QGraphicsView
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt


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
        self.cover= GetCover(self.sp)

        # Set up the window
        self.setWindowTitle("The Frame")
        self.setGeometry(100, 100, 1920, 1080)

        # Set the background image to cover.jpg with a stronger blur effect
        self.set_background_image("cover.jpg", blur_radius=500, overlay_alpha=1)

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
        title_label_title = QLabel(self)
        title_label_title.setStyleSheet("color: #222222; font-size: 16px; font-weight: bold;")
        title_label_title.setAlignment(Qt.AlignCenter)
        title_label_title.setText(CurrentlyPlaying(self.sp)["title"])
        grid_layout.addWidget(title_label_title, 2, 1)

        # Set Artist
        title_label_artist = QLabel(self)
        title_label_artist.setStyleSheet("color: #3b3b3b; font-size: 14px;")
        title_label_artist.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        title_label_artist.setText(CurrentlyPlaying(self.sp)["artist"])
        grid_layout.addWidget(title_label_artist, 3, 1)

        # Insert an image in Row 2, Column 2
        image_label = QLabel(self)
        image_pixmap = QPixmap("cover.jpg")  # Replace with your image file path
        image_label.setPixmap(image_pixmap)  # Adjust width as needed
        image_label.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(image_label, 1, 1, 1, 1)  # Span one row and one column


        self.setLayout(grid_layout)



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