
import os
import logging
from PyQt6.QtGui import QIcon, QImage, QPixmap, QPainter, QPalette, QColor
from PyQt6.QtCore import pyqtSignal, Qt, QEvent, pyqtProperty
from PyQt6.QtWidgets import QPushButton, QApplication
from app.core.config import configs


class QIconButton(QPushButton):
    onclick = pyqtSignal()

    def __init__(self, icon_file, tool_tip):
        super().__init__(None)

        self.setToolTip(tool_tip)

        self.clicked.connect(self.on_click)

        self._iconcolor = QColor.fromString('black')
        self.setIconFile(icon_file)

    def on_click(self):
        print("Обработчик не определен")

    @pyqtProperty(QColor)
    def iconcolor(self):
        return self._iconcolor
 
    @iconcolor.setter
    def iconcolor(self, iconcolor):
        self._iconcolor = iconcolor
        self.update_icon()

    def setIconFile(self, icon_file):
        self.image = QImage(os.path.join(configs.RESOURCES_DIR, icon_file))
        self.image.convertTo(QImage.Format.Format_ARGB32)
        self.setImage(self.image)

    def setImage(self, image):
        pixmap = QPixmap.fromImage(image)
        icon = QIcon(pixmap)
        super().setIcon(icon)

    def update_icon(self):
        image = self.image.copy()
        color = self._iconcolor

        for y in range(image.height()):
            for x in range(image.width()):
                pixel_color = image.pixelColor(x, y)
                if pixel_color == Qt.GlobalColor.black:
                    image.setPixelColor(x, y, color)
                
        self.setImage(image)

