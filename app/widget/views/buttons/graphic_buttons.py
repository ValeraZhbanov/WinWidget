
import os
from app.widget.views.buttons.icon_button import QIconButton
from app.service.drawing_manager import DrawingManager, Rectangle, Arrow
from app.service.toast_manager import ToastManager
from app.core.config import configs



class RectangleButton(QIconButton):
    def __init__(self):
        super().__init__("icons8-rectangle-80.png", "Нарисовать прямоугольник")
        
    def on_click(self):
        DrawingManager().new_figure(Rectangle)


class ArrowButton(QIconButton):
    def __init__(self):
        super().__init__("icons8-arrow-50.png", "Нарисовать стрелку")
        
    def on_click(self):
        DrawingManager().new_figure(Arrow)


class CleanButton(QIconButton):
    def __init__(self):
        super().__init__("icons8-clean-50.png", "Нарисовать стрелку")
        
    def on_click(self):
        DrawingManager().clean()