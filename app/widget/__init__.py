import sys
import logging
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication
from app.service.drawing_manager import DrawingManager
from app.service.overlay_manager import OverlayManager
from app.core.config import configs


class QWinWidgetApplication(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

    def event(self, event: QEvent):
        if event.type() in (QEvent.Type.ApplicationPaletteChange,):
            self.loadQssStyle()

        return super().event(event)
        
    def loadQssStyle(self):
        logging.debug('Load qss styles')
        with open(configs.STYLES_PATH, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())


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

        self.app = QWinWidgetApplication(sys.argv)
        self.app.setStyle("Fusion")

        self.drawing_manager = DrawingManager()
        self.overlay_manager = OverlayManager()

    def run(self):
        sys.exit(self.app.exec())
