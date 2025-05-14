
import logging
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QObject, QTimer, QRect, pyqtSignal
from PyQt6.QtGui import QCursor, QPainter, QColor, QPen
from PyQt6.QtWidgets import QWidget
from app.core.config import configs


class OverlayManager(QObject):
    activation_changed = pyqtSignal(bool)

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

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_position)
        self.is_active = False

        self.target_rect = QRect(*configs.TARGET_RECT)
        self.widget_rect = QRect(*configs.WIDGET_RECT)
        
        self.overlay = QWidget()
        self.overlay.setAccessibleName("OverlayWidget")

        self.overlay.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput
        )

        self.overlay.setGeometry(self.target_rect)
        self.overlay.show()

    def start(self):
        self.timer.start(configs.MOUSE_INTERVAL_UPDATE)
        logging.info("Mouse tracking started")

    def stop(self):
        self.timer.stop()
        self.overlay.close()
        logging.info("Mouse tracking stopped")

    def check_position(self):
        pos = QCursor.pos()
        self.overlay.update()

        if self.target_rect.contains(pos) or (self.is_active and self.widget_rect.contains(pos)):
            if not self.is_active:
                self.is_active = True
                self.activation_changed.emit(True)
                logging.debug(f"Mouse in target area {pos}")

        else:
            if self.is_active:
                self.is_active = False
                self.activation_changed.emit(False)
                logging.debug(f"Mouse outside area {pos}")