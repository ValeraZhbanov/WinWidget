
from PyQt6.QtWidgets import QFrame


class QSeparator(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setStyleSheet("background-color: #555;")
        self.setFixedHeight(1)
