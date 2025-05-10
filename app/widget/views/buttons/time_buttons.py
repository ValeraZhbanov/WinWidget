
from PyQt6.QtWidgets import QInputDialog
from app.widget.views.buttons.base_button import BaseButton
from app.service.timer_service import TimerService


class TimerButton(BaseButton):
    def __init__(self):
        super().__init__("icons8-timer-50.png", "Установить таймер")
        self.timer_service = TimerService()

    def on_click(self):
        minutes, ok = QInputDialog.getInt(self.window(), "Таймер", "Минут:", 1, 1, 120)
        if ok:
            self.timer_service.start_timer(minutes * 60)