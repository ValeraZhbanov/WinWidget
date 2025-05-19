import logging
from PyQt6.QtCore import Qt, QObject, QRect, pyqtSignal, QEvent, QTimer
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QApplication, QLineEdit, QTextEdit, QComboBox, QSpinBox, QDateTimeEdit
from app.views.main_widget import QMainWidget
from app.views.qelements import QHoveredWidget
from app.config import configs


class QOverlayWidget(QHoveredWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("OverlayWidget")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setGeometry(*configs.TARGET_RECT)


class OverlayService(QObject):

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

        self.target_rect = QRect(*configs.TARGET_RECT)
        self.widget_rect = QRect(*configs.WIDGET_RECT)
        
        self.overlay = QOverlayWidget()
        self.overlay.show()

        self.main = QMainWidget()
        self.main.hide()

        self.overlay.mouse_enter.connect(self.main_show)

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_visible_conditions)
        self.timer.setInterval(configs.MOUSE_INTERVAL_UPDATE)

    def main_show(self):

        if self.main.isVisible():
            return        

        self.main.show()
        self.timer.start()

    def check_visible_conditions(self):
        logging.debug(f"Mouse position check")
        pos = QCursor.pos()
        self.overlay.update()

        if self.target_rect.contains(pos) or (self.main.isVisible() and self.widget_rect.contains(pos)) or self.app_has_focus():
            if not self.main.isVisible():
                self.main.show()
                logging.debug(f"Mouse in target area {pos}")

        else:
            if self.main.isVisible():
                self.main.hide()
                self.timer.stop()
                logging.debug(f"Mouse outside area {pos}")

    def app_has_focus(self):
        app = QApplication.instance()
        current_widget = app.focusWidget()
        input_widget_classes = (QLineEdit, QTextEdit, QComboBox, QSpinBox, QDateTimeEdit)
    
        if not current_widget:
            return False

        return isinstance(current_widget, input_widget_classes)

        