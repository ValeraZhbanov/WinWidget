import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from app.service.drawing_manager import DrawingManager
from app.service.overlay_manager import OverlayManager
from app.widget.views.base_frame import BaseFrame


class WinWidget:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.is_visible = False

        self.drawing_manager = DrawingManager()

        self.overlay_manager = OverlayManager()
        self.overlay_manager.activation_changed.connect(self.toggle_widget)
        self.overlay_manager.start()

        self.frame = BaseFrame()
        self.frame.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

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
