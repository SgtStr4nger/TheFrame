from API_Access import CurrentlyPlaying, GetCover

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QWidget, QGraphicsBlurEffect
from PyQt5.QtGui import QPixmap, QColor, QPalette,  QBrush
from PyQt5.QtCore import Qt

class GridLayoutExample(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("Grid Layout Example")
        self.setGeometry(100, 100, 800, 800)

        # Create a grid layout with 4 rows and 3 columns
        grid_layout = QGridLayout(self)

        # Set the background image to cover.jpg scaled to the window size with a stronger blur effect
        self.set_background_image("cover.jpg")

        # Add widgets to the grid
        for row in range(6):
            for col in range(3):
                grid_layout.addWidget(QLabel(""), row, col)

        # Set the width of the second column to a fixed width of 640
        grid_layout.setColumnMinimumWidth(1, 640)
        grid_layout.setColumnStretch(1, 0)  # Disable stretching for the second column

        # Set Title
        title_label_title = QLabel(self)
        title_label_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        title_label_title.setAlignment(Qt.AlignCenter)
        title_label_title.setText(CurrentlyPlaying()["title"])
        grid_layout.addWidget(title_label_title, 2, 1)

        # Set Artist
        title_label_artist = QLabel(self)
        title_label_artist.setStyleSheet("color: #b0b0b0; font-size: 14px;")
        title_label_artist.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        title_label_artist.setText(CurrentlyPlaying()["artist"])
        grid_layout.addWidget(title_label_artist, 3, 1)

        # Insert an image in Row 2, Column 2
        image_label = QLabel(self)
        image_pixmap = QPixmap("cover.jpg")  # Replace with your image file path
        image_label.setPixmap(image_pixmap)  # Adjust width as needed
        image_label.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(image_label, 1, 1, 1, 1)  # Span one row and one column

        self.setLayout(grid_layout)

    def set_background_image(self, image_path):
        # Load the cover image
        cover_pixmap = QPixmap(image_path)
        scaled_cover_pixmap = cover_pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # Blur effect with stronger radius
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(50)  # Adjust the value for a stronger blur effect

        # Darken the background with a semi-transparent overlay
        overlay_color = QColor(0, 0, 0, 100)  # Adjust the alpha value for darkness
        overlay_pixmap = QPixmap(self.size())
        overlay_pixmap.fill(overlay_color)

        # Create a label for the background image
        background_label = QLabel(self)
        background_label.setPixmap(scaled_cover_pixmap)
        background_label.setAlignment(Qt.AlignCenter)
        background_label.setGraphicsEffect(blur)

        # Set up the palette with the background label and overlay
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(background_label.pixmap()))
        palette.setBrush(QPalette.WindowText, QBrush(overlay_pixmap))  # Use WindowText for overlay
        self.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GridLayoutExample()
    window.show()
    sys.exit(app.exec_())
    sys.exit(app.exec_())