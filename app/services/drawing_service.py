import logging
import ctypes
from ctypes import wintypes
from PyQt6.QtCore import QObject, QRect, QPoint, Qt, QEvent, pyqtSignal, QTimer
from PyQt6.QtGui import QColor, QMouseEvent, QPainter, QPen, QBrush, QPolygon
from PyQt6.QtWidgets import QApplication, QWidget
from typing import Set


user32 = ctypes.windll.user32

class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("pt", wintypes.POINT),
        ("mouseData", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.PULONG)
    ]


class Figure:
    def __init__(self):
        self.pen_color = QColor(255, 0, 0)
        self.pen_width = 2
        self.style_args = {}

    def draw(self, painter: QPainter):
        raise NotImplementedError("Subclasses must implement this method")


class Rectangle(Figure):
    def __init__(self, point1: QPoint, point2: QPoint):
        super().__init__()
        self.rect = QRect(point1, point2)
        self.pen_color = QColor(0, 255, 0)
        self.style_args = {"filled": False}

    def draw(self, painter: QPainter):
        painter.setPen(QPen(self.pen_color, self.pen_width))

        if self.style_args.get("filled", False):
            painter.setBrush(QBrush(self.pen_color))
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.drawRect(self.rect)


class Arrow(Figure):
    def __init__(self, point1: QPoint, point2: QPoint):
        super().__init__()
        self.point1 = point1
        self.point2 = point2
        self.pen_color = QColor(255, 0, 0)
        self.pen_width = 3
        self.style_args = {"arrow_size": 10}

    def draw(self, painter: QPainter):
        painter.setPen(QPen(self.pen_color, self.pen_width))
        painter.drawLine(self.point1, self.point2)
        self._draw_arrow_head(painter)

    def _draw_arrow_head(self, painter: QPainter):
        arrow_size = self.style_args.get("arrow_size", 10)
        dx = self.point2.x() - self.point1.x()
        dy = self.point2.y() - self.point1.y()
        length = (dx**2 + dy**2)**0.5

        if length == 0:
            return

        dx /= length
        dy /= length
        
        perp_x = -dy
        perp_y = dx

        arrow_point1 = QPoint(
            int(self.point2.x() - arrow_size * dx + arrow_size * 0.5 * perp_x),
            int(self.point2.y() - arrow_size * dy + arrow_size * 0.5 * perp_y)
        )

        arrow_point2 = QPoint(
            int(self.point2.x() - arrow_size * dx - arrow_size * 0.5 * perp_x),
            int(self.point2.y() - arrow_size * dy - arrow_size * 0.5 * perp_y)
        )

        arrow_head = QPolygon([self.point2, arrow_point1, arrow_point2])
        painter.setBrush(QBrush(self.pen_color))
        painter.drawPolygon(arrow_head)


class DrawingOverlay(QWidget):
    def __init__(self, drawing_service):
        super().__init__()
        self.drawing_service = drawing_service
        self.hook_id = None
        self.is_drawing = False
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        self.setCursor(Qt.CursorShape.CrossCursor)   

    def install_hook(self):

        def hook_callback(nCode, wParam, lParam):
            if nCode >= 0:
                event = ctypes.cast(lParam, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
                pos = QPoint(event.pt.x, event.pt.y)
                
                if wParam == 0x0201:  # WM_LBUTTONDOWN
                    self.is_drawing = True
                    self.drawing_service.start_new_figure(pos)
                    return 1
                
                elif wParam == 0x0200 and self.is_drawing:  # WM_MOUSEMOVE
                    self.drawing_service.update_current_figure(pos)
                    self.drawing_service.overlay.update()
                
                elif wParam == 0x0202:  # WM_LBUTTONUP
                    if self.is_drawing:
                        self.is_drawing = False
                        self.drawing_service.finish_figure()
                        return 1
            
            return user32.CallNextHookEx(self.hook_id, nCode, wParam, lParam)

        CMPFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))
        self.hook_callback = CMPFUNC(hook_callback)
        self.hook_id = user32.SetWindowsHookExA(14, self.hook_callback, None, 0)
        logging.debug(f"Mouse hook install")

    def update(self):
        super().update()

        if 0 < len(self.drawing_service.figures) or self.drawing_service.current_figure is not None:
            if not self.isVisible():
                self.show()
        else:
            if self.isVisible():
                QTimer.singleShot(50, self.hide) 

    def remove_hook(self):
        if self.hook_id:
            user32.UnhookWindowsHookEx(self.hook_id)
            self.hook_id = None
            logging.debug(f"Mouse hook drop")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        for figure in self.drawing_service.figures:
            figure.draw(painter)
            
        if self.drawing_service.current_figure:
            self.drawing_service.current_figure.draw(painter)
            
        painter.end()

    def closeEvent(self, event):
        self.remove_hook()
        super().closeEvent(event)


class DrawingService(QObject):
    _instance = None

    finish_figure_signal = pyqtSignal(object)

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
        
        self.figures: Set[Figure] = set()
        self.overlay = DrawingOverlay(self)
        self.overlay.hide()
        
        self.current_figure_start = None
        self.current_figure_type = None
        self.current_figure = None

    def overlay_update(self):
        self.overlay.update()

    def new_figure(self, FigureType):
        self.reset_state()
        self.current_figure_type = FigureType
        self.overlay.install_hook()
        self.overlay.update()
        logging.debug(f"New figure mode: {FigureType.__name__}")

    def remove_figure(self, figure):
        if figure in self.figures:
            self.figures.remove(figure)
            self.overlay.update()
            logging.debug(f"Figure removed: {figure}")
            return True
        return False

    def start_new_figure(self, pos):
        if self.current_figure_type:
            self.current_figure_start = pos
            logging.debug(f"Start new figure at {pos}")

    def update_current_figure(self, pos):
        if self.current_figure_start and self.current_figure_type:
            self.current_figure = self.current_figure_type(self.current_figure_start, pos)
            self.overlay.update()

    def finish_figure(self):
        if self.current_figure:
            self.figures.add(self.current_figure)
            self.finish_figure_signal.emit(self.current_figure)
            logging.debug(f"Finish new figure")
        self.reset_state()
        self.overlay.update()

    def clean(self):
        self.figures.clear()
        self.reset_state()
        self.overlay.update()
        logging.debug("All figures cleared")

    def reset_state(self):
        self.current_figure = None
        self.current_figure_start = None
        self.current_figure_type = None
        self.overlay.remove_hook()
        logging.debug("Drawing state reset")



