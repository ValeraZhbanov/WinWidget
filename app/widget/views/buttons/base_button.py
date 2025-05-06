
import os
from PyQt6.QtGui import QIcon, QImage, QPixmap, QPainter
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QPushButton
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

        image = QImage(icon_path)
            
        image.invertPixels(QImage.InvertMode.InvertRgb)
            
        pixmap = QPixmap.fromImage(image)
        icon = QIcon(pixmap)
        
        super().setIcon(icon)
        

