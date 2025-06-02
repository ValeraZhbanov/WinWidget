
import sys
import logging
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QApplication
from app.services.drawing_service import DrawingService
from app.services.overlay_service import OverlayService
from app.services.integration_service import IntegrationService
from app.services.timer_service import TimerService
from app.services.toast_service import ToastService
from app.core.config import configs


class WinWidget(QApplication):
    def __init__(self):

        logging.basicConfig(stream=sys.stdout, level=configs.LOGGING_LEVEL)

        super().__init__(sys.argv)
        self.setStyle("Fusion")

        self.drawing_service = DrawingService()
        self.overlay_service = OverlayService()
        self.integration_service = IntegrationService()
        self.timer_service = TimerService()
        self.toast_service = ToastService()

    def event(self, event: QEvent):
        if event.type() in (QEvent.Type.ApplicationPaletteChange,):
            self.loadQssStyle()

        return super().event(event)
        
    def loadQssStyle(self):
        logging.debug('Load qss styles')
        with open(configs.STYLES_PATH, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

