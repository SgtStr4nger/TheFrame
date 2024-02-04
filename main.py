import sys

from PyQt5.QtWidgets import QApplication
from Spotify.Displaying_white_edition import TheFrame_Spotify





if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = TheFrame_Spotify()
    window.show()
    sys.exit(app.exec_())

