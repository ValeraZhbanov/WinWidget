import sys
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

        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion")

        palette = self.app.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(43, 43, 43))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(58, 58, 58))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(46, 46, 46))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(58, 58, 58))
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(58, 58, 58))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(10, 120, 10))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        self.app.setPalette(palette)

        with open(configs.STYLES_PATH, "r", encoding="utf-8") as f:
            self.app.setStyleSheet(f.read())

        self.drawing_manager = DrawingManager()
        self.overlay_manager = OverlayManager()

    def run(self):
        sys.exit(self.app.exec())
