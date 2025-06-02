
import os
from app.core.base_action import BaseAction
from app.services.drawing_service import DrawingService, Rectangle, Arrow


class RectangleDrawAction(BaseAction):
    group: str = 'DRAW'
    order: int = 1

    icon_path: str | None = 'icons8-rectangle-80.png'
    title: str | None = 'Прямоугольник'
    description: str | None = 'Нарисовать прямоугольник'
        
    def perform(self):
        DrawingService().new_figure(Rectangle)


class ArrowDrawAction(BaseAction):
    group: str = 'DRAW'
    order: int = 2

    icon_path: str | None = 'icons8-arrow-50.png'
    title: str | None = 'Стрелка'
    description: str | None = 'Нарисовать стрелку'
        
    def perform(self):
        DrawingService().new_figure(Arrow)


class CleanDrawedAction(BaseAction):
    group: str = 'DRAW'
    order: int = 3

    icon_path: str | None = 'icons8-clean-50.png'
    title: str | None = 'Очистить'
    description: str | None = 'Убрать все нарисованные объекты'
      
    def perform(self):
        DrawingService().clean()