import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from app.service.drawing_manager import DrawingManager
from app.service.overlay_manager import OverlayManager
from app.widget.views.base_frame import BaseFrame


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
        self.is_visible = False

        self.drawing_manager = DrawingManager()

        self.overlay_manager = OverlayManager()
        self.overlay_manager.activation_changed.connect(self.toggle_widget)
        self.overlay_manager.start()

        self.frame = BaseFrame()
        self.frame.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

    def get_main_window():
        return self.frame

    def toggle_widget(self, is_visible):

        if self.is_visible == is_visible:
            return

        self.is_visible = is_visible

        if self.is_visible:
            self.frame.animation.start()
        else:
            self.frame.disappear_animation.start()

        self.frame.setVisible(self.is_visible)

    def run(self):
        sys.exit(self.app.exec())
