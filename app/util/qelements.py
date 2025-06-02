
from PyQt6.QtGui import QIcon, QImage, QPixmap, QColor
from PyQt6.QtCore import pyqtSignal, Qt, QEvent, pyqtProperty
from PyQt6.QtWidgets import QDialog, QFrame, QPushButton


class QHSeparator(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setFixedHeight(1)


class QVSeparator(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setFixedWidth(1)


class QEmpty(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShadow(QFrame.Shadow.Sunken)


class QIconButton(QPushButton):
    onclick = pyqtSignal()

    def __init__(self, icon_file, tool_tip):
        super().__init__(None)

        self.setToolTip(tool_tip)

        self.clicked.connect(self.on_click)

        self._iconcolor = QColor.fromString('black')
        self.setIconFile(icon_file)

    def on_click(self):
        print("Обработчик не определен")

    @pyqtProperty(QColor)
    def iconcolor(self):
        return self._iconcolor
 
    @iconcolor.setter
    def iconcolor(self, iconcolor):
        self._iconcolor = iconcolor
        self.update_icon()

    def setIconFile(self, icon_file):
        self.image = QImage(icon_file)
        self.image.convertTo(QImage.Format.Format_ARGB32)
        self.setImage(self.image)

    def setImage(self, image):
        pixmap = QPixmap.fromImage(image)
        icon = QIcon(pixmap)
        super().setIcon(icon)

    def update_icon(self):
        image = self.image.copy()
        color = self._iconcolor

        for y in range(image.height()):
            for x in range(image.width()):
                pixel_color = image.pixelColor(x, y)
                pixel_color.setRed(color.red())
                pixel_color.setGreen(color.green())
                pixel_color.setBlue(color.blue())
                image.setPixelColor(x, y, pixel_color)
                
        self.setImage(image)


class QDialogParentHide(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Dialog
        )
        self.setGeometry(parent.geometry())
        parent.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Hide:
            self.reject()
        return super().eventFilter(obj, event)


class QHoveredWidget(QFrame):
    mouse_enter = pyqtSignal()
    mouse_leave = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

    def enterEvent(self, a0):
        self.mouse_enter.emit()
        return super().enterEvent(a0)

    def leaveEvent(self, a0):
        self.mouse_leave.emit()
        return super().leaveEvent(a0)

