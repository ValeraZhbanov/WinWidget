from datetime import timedelta
from PyQt6.QtWidgets import QInputDialog
from app.views.qelements import QIconButton
from app.services.timer_service import TimerService
from app.services.toast_service import ToastService
from app.views.dialogs.timer_dialogs import TimerDialog, TimersListDialog


class TimerQuick10Button(QIconButton):
    def __init__(self):
        super().__init__('icons8-10-50.png', 'Таймер на 10 минут')
        
    def on_click(self):
        TimerService().add_duration_timer(timedelta(minutes=10))
        ToastService().add(f'Таймер установлен на 10 минут')


class TimerQuick30Button(QIconButton):
    def __init__(self):
        super().__init__('icons8-30-50.png', 'Таймер на 30 минут')
        
    def on_click(self):
        TimerService().add_duration_timer(timedelta(minutes=30))
        ToastService().add(f'Таймер установлен на 30 минут')


class TimerQuick60Button(QIconButton):
    def __init__(self):
        super().__init__('icons8-60-50.png', 'Таймер на 60 минут')
        
    def on_click(self):
        TimerService().add_duration_timer(timedelta(minutes=60))
        ToastService().add(f'Таймер установлен на 60 минут')


class TimerDialogButton(QIconButton):
    def __init__(self):
        super().__init__('icons8-timer-50.png', 'Добавить таймер')
        
    def on_click(self):
        dialog = TimerDialog(self.window())
        dialog.exec()


class TimersListButton(QIconButton):
    def __init__(self):
        super().__init__('icons8-bulleted-list-100.png', 'Список таймеров')
        
    def on_click(self):
        dialog = TimersListDialog(self.window())
        dialog.exec()