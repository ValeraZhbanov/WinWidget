
import logging
from PyQt6.QtWidgets import QInputDialog
from app.widget.views.buttons.base_button import BaseButton
from app.service.ocr_service import OCRService
from app.service.drawing_manager import DrawingManager, Rectangle


class OCRButton(BaseButton):
    def __init__(self):
        super().__init__("icons8-ocr-50.png", "Распознать текст с экрана")
        self.drawing_manager = DrawingManager()

    def on_click(self):
        self.drawing_manager.new_figure(Rectangle)
        self.drawing_manager.finish_figure_signal.connect(self._on_figure_finished)

    def _on_figure_finished(self, figure):
        if isinstance(figure, Rectangle):
            rect = figure.rect
            if OCRService().capture_and_recognize(rect):
                logging.info("Text recognized and copied to clipboard")
            self.drawing_manager.remove_figure(figure)