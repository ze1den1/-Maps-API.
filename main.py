import sys

from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

from mapImage import MapImage

SCREEN_SIZE = (600, 450)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('forms/mainWindow.ui', self)
        self._map = MapImage()
        self.getImage()

    def getImage(self):
        pixmap = QPixmap()
        image = self._map.image

        if image is None:
            QMessageBox(QMessageBox.Icon.Warning, 'WARNING!', 'Не удалось загрузить карту')
        else:
            pixmap.loadFromData(image, format='PNG')
        self.image.setPixmap(pixmap)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
