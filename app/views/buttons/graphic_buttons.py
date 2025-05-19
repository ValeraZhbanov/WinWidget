
import os
from app.views.qelements import QIconButton
from app.services.drawing_service import DrawingService, Rectangle, Arrow
from app.services.toast_service import ToastService
from app.config import configs


class RectangleButton(QIconButton):
    def __init__(self):
        super().__init__("icons8-rectangle-80.png", "Нарисовать прямоугольник")
        
    def on_click(self):
        DrawingService().new_figure(Rectangle)


class ArrowButton(QIconButton):
    def __init__(self):
        super().__init__("icons8-arrow-50.png", "Нарисовать стрелку")
        
    def on_click(self):
        DrawingService().new_figure(Arrow)


class CleanButton(QIconButton):
    def __init__(self):
        super().__init__("icons8-clean-50.png", "Нарисовать стрелку")
        
    def on_click(self):
        DrawingService().clean()