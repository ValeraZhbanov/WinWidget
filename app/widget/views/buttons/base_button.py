
import os
from PyQt6.QtGui import QIcon, QImage, QPixmap, QPainter, QPalette
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QPushButton, QApplication
from app.core.config import configs

class BaseButton(QPushButton):
    onclick = pyqtSignal()

    def __init__(self, icon_file, tool_tip):
        super().__init__(None)
        self.setToolTip(tool_tip)
        self.setIcon(os.path.join(configs.RESOURCES_DIR, icon_file))
        self.clicked.connect(self.on_click)

    def on_click(self):
        print("Обработчик не определен")


    def setIcon(self, icon_path):
        app: QApplication = QApplication.instance()
        palette: QPalette = app.palette()
        color = palette.color(QPalette.ColorGroup.Normal, QPalette.ColorRole.ButtonText)

        image = QImage(icon_path)
            
        image.convertTo(QImage.Format.Format_ARGB32)

        for y in range(image.height()):
            for x in range(image.width()):
                pixel_color = image.pixelColor(x, y)
                if pixel_color == Qt.GlobalColor.black:
                    image.setPixelColor(x, y, color)
                
        pixmap = QPixmap.fromImage(image)
        icon = QIcon(pixmap)
        
        super().setIcon(icon)
        

