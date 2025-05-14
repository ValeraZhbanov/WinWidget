import os
from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect
from app.widget.views.datetime_view import DateTimeView
from app.widget.views.buttons import ButtonsGroup
from app.widget.utils.qelements import QSeparator
from app.core.config import configs

class BaseFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName('MainFrame')
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setGeometry(QRect(*configs.WIDGET_RECT))
        self.setFixedSize(*configs.WIDGET_RECT[2:])

        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)

        self.disappear_animation = QPropertyAnimation(self, b"windowOpacity")
        self.disappear_animation.setDuration(300)
        self.disappear_animation.setStartValue(1)
        self.disappear_animation.setEndValue(0)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(3, 3)
        shadow.setColor(Qt.GlobalColor.gray)
        self.setGraphicsEffect(shadow)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)

        self.datetime_view = DateTimeView()
        self.main_layout.addWidget(self.datetime_view)

        self.separator = QSeparator()
        self.main_layout.addWidget(self.separator)
        
        self.buttons_group = ButtonsGroup()
        self.main_layout.addWidget(self.buttons_group)

        self.setLayout(self.main_layout)