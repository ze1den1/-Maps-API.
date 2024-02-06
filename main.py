import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QKeyEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

from mapImage import MapImage, MapType

SCREEN_SIZE = (600, 450)


class MainWindow(QMainWindow):
    SCALE_COEFF = 2

    def __init__(self):
        super().__init__()
        uic.loadUi('forms/mainWindow.ui', self)

        self._map = MapImage()
        self.updateImage()
        self.layerGroup.buttonClicked.connect(self.select_layer)

    def select_layer(self):
        match self.layerGroup.checkedButton():
            case self.radioSchema:
                self._map.set_type(MapType.SCHEMA)
            case self.radioSatellite:
                self._map.set_type(MapType.SATELLITE)
            case self.radioHybrid:
                self._map.set_type(MapType.HYBRID)
        self.updateImage()
        self.focusWidget().clearFocus()

    def updateImage(self):
        pixmap = QPixmap()
        image = self._map.image

        if image is None:
            QMessageBox(QMessageBox.Icon.Warning, 'WARNING!', 'Не удалось загрузить карту',
                        QMessageBox.StandardButton.NoButton, self).show()
        else:
            pixmap.loadFromData(image)
        self.image.setPixmap(pixmap)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        match event.key():
            case Qt.Key.Key_PageUp:
                self._map.scaling(1 / self.SCALE_COEFF)
            case Qt.Key.Key_PageDown:
                self._map.scaling(self.SCALE_COEFF)
            case Qt.Key.Key_Up:
                self._map.screen_up()
            case Qt.Key.Key_Down:
                self._map.screen_down()
            case Qt.Key.Key_Left:
                self._map.screen_left()
            case Qt.Key.Key_Right:
                self._map.screen_right()
        if event.key() in (
                Qt.Key.Key_PageUp, Qt.Key.Key_PageDown, Qt.Key.Key_Up, Qt.Key.Key_Down, Qt.Key.Key_Left,
                Qt.Key.Key_Right
        ):
            self.updateImage()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
