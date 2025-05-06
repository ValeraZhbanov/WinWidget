
import os
from app.widget.views.buttons.base_button import BaseButton
from app.service.drawing_manager import DrawingManager, Rectangle, Arrow
from app.core.config import configs



class RectangleButton(BaseButton):
    def __init__(self):
        super().__init__("icons8-rectangle-80.png", "Нарисовать прямоугольник")
        
    def on_click(self):
        DrawingManager().new_figure(Rectangle)


class ArrowButton(BaseButton):
    def __init__(self):
        super().__init__("icons8-arrow-50.png", "Нарисовать стрелку")
        
    def on_click(self):
        DrawingManager().new_figure(Arrow)


class CleanButton(BaseButton):
    def __init__(self):
        super().__init__("icons8-clean-50.png", "Нарисовать стрелку")
        
    def on_click(self):
        DrawingManager().clean()