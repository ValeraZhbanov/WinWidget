import os
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect
from app.views.datetime_widget import QDateTimeWidget
from app.views.action_frame import ActionFrame
from app.util.qelements import QHSeparator, QHoveredWidget
from app.core.config import configs


class QMainWidget(QHoveredWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setMouseTracking(True)
        self.setGeometry(QRect(*configs.WIDGET_RECT))
        self.setFixedSize(*configs.WIDGET_RECT[2:])
        
        self.animation_show = QPropertyAnimation(self, b"windowOpacity")
        self.animation_show.setDuration(300)
        self.animation_show.setStartValue(0)
        self.animation_show.setEndValue(1)

        self.animation_hide = QPropertyAnimation(self, b"windowOpacity")
        self.animation_hide.setDuration(300)
        self.animation_hide.setStartValue(1)
        self.animation_hide.setEndValue(0)
        self.animation_hide.finished.connect(self._on_hide_finished)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(3, 3)
        shadow.setColor(Qt.GlobalColor.gray)
        self.setGraphicsEffect(shadow)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.datetime_view = QDateTimeWidget()
        self.main_layout.addWidget(self.datetime_view)

        self.separator = QHSeparator()
        self.main_layout.addWidget(self.separator)
        
        self.buttons_group = ActionFrame()
        self.main_layout.addWidget(self.buttons_group)

        self.setLayout(self.main_layout)

    def show(self):
        self.datetime_view.start()
        self.animation_show.start()
        self.raise_()
        self.activateWindow()
        return super().show()

    def hide(self):
        self.animation_hide.start()

    def _on_hide_finished(self):
        self.datetime_view.stop()
        return super().hide()