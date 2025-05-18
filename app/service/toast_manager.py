import logging
from PyQt6.QtCore import Qt, QObject, QRect, pyqtSignal, QEvent, QTimer, QPropertyAnimation, QPoint, QLocale, QDateTime, pyqtProperty
from PyQt6.QtGui import QCursor, QColor, QPalette
from PyQt6.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QSizePolicy
from app.widget.utils.qelements import QHoveredWidget
from app.core.config import configs


class ToastMessage(QFrame):
    def __init__(self, text, parent):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        self._opacity = 0

        self.animation_show = QPropertyAnimation(self, b"opacity")
        self.animation_show.setStartValue(0)
        self.animation_show.setEndValue(0.8)
        self.animation_show.setDuration(300)
        self.animation_show.finished.connect(self._on_show_finished)

        self.animation_hide = QPropertyAnimation(self, b"opacity")
        self.animation_hide.setStartValue(1)
        self.animation_hide.setEndValue(0.8)
        self.animation_hide.setDuration(300)
        self.animation_hide.finished.connect(self._on_hide_finished)
        
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

        self.locale = QLocale()

        current_time = QDateTime.currentDateTime()

        self.layout = QVBoxLayout()

        time_label = QLabel(self.locale.toString(current_time, configs.TIME_FORMAT), self)
        time_label.setObjectName('TimeLabel')
        self.layout.addWidget(time_label)

        message_label = QLabel(text, self)
        message_label.setObjectName('MessageLabel')
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(message_label)

        self.setLayout(self.layout)

        self._update_style()

    @pyqtProperty(float)
    def opacity(self):
        return self._opacity
 
    @opacity.setter
    def opacity(self, opacity):
        self._opacity = opacity
        self._update_style()

    def _update_style(self):
        palette:QPalette = self.palette()
        color_dark = palette.color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Dark)
        color_mid = palette.color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Mid)
        color_text = palette.color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Text)

        color_dark.setAlphaF(self.opacity)
        color_mid.setAlphaF(self.opacity)
        color_text.setAlphaF(self.opacity)

        color_dark = f'rgba({color_dark.red()}, {color_dark.green()}, {color_dark.blue()}, {color_dark.alpha()})'
        color_mid = f'rgba({color_mid.red()}, {color_mid.green()}, {color_mid.blue()}, {color_mid.alpha()})'
        color_text = f'rgba({color_text.red()}, {color_text.green()}, {color_text.blue()}, {color_text.alpha()})'

        self.setStyleSheet(f"""
        #ToastWidget ToastMessage {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {color_dark}, stop:1 {color_mid});
            color: {color_text};
        }}

        #ToastWidget ToastMessage:hover {{
            background: palette(dark); 
            color: palette(text);
        }}
            
        """)

    def show(self):
        self.opacity = 0
        super().show()
        self.animation_show.start()
        logging.debug('Toast add')

    def hide(self):
        self.timer.stop()
        self.animation_hide.start()
        logging.debug('Toast hide')

    def hide_fast(self):
        self.timer.stop()
        self._on_hide_finished()
        logging.debug('Toast hide fast')

    def _on_show_finished(self):
        self.timer.start(3000)
        logging.debug('Toast timer start')

    def _on_hide_finished(self):
        super().hide()
        self.deleteLater()
        logging.debug('Toast deleted')


class QToastWidget(QHoveredWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ToastWidget")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool 
        )
        self.setGeometry(*configs.TOAST_RECT)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        

    def add_message(self, text):
        message = ToastMessage(text, self)
        self.layout.insertWidget(0, message)
        message.show()
        logging.debug(f'Toast messages count {self.layout.count()}')

        if self.layout.count() > 10:
            oldest = self.layout.itemAt(self.layout.count() - 1).widget()
            if oldest:
                oldest.hide_fast()


class ToastManager(QObject):

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

        self.toast_widget = QToastWidget()
        self.toast_widget.show()

    def add(self, message):
        self.toast_widget.add_message(message)
