import sys
import logging
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication
from app.service.drawing_manager import DrawingManager
from app.service.overlay_manager import OverlayManager
from app.core.config import configs


class WinWidget:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        super().__init__()
        self.__initialized = True

        logging.basicConfig(level=configs.LOGGING_LEVEL)

        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion")

        with open(configs.STYLES_PATH, "r", encoding="utf-8") as f:
            self.app.setStyleSheet(f.read())

        self.drawing_manager = DrawingManager()
        self.overlay_manager = OverlayManager()

    def run(self):
        sys.exit(self.app.exec())
