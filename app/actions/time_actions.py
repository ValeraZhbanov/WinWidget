from datetime import timedelta
from app.core.base_action import BaseAction
from app.services.timer_service import TimerService
from app.services.toast_service import ToastService
from app.views.dialogs.timer_dialogs import TimerDialog, TimersListDialog

        
class TimerQuick10Action(BaseAction):
    group: str = 'TIME'
    order: int = 1

    icon_path: str | None = 'icons8-10-50.png'
    title: str | None = '10 минут'
    description: str | None = 'Таймер на 10 минут'

    def perform(self):
        TimerService().add_duration_timer(timedelta(minutes=10))
        ToastService().add(f'Таймер установлен на 10 минут')

      
class TimerQuick30Action(BaseAction):
    group: str = 'TIME'
    order: int = 2

    icon_path: str | None = 'icons8-30-50.png'
    title: str | None = '30 минут'
    description: str | None = 'Таймер на 30 минут'

    def perform(self):
        TimerService().add_duration_timer(timedelta(minutes=30))
        ToastService().add(f'Таймер установлен на 30 минут')

        
class TimerQuick60Action(BaseAction):
    group: str = 'TIME'
    order: int = 2

    icon_path: str | None = 'icons8-60-50.png'
    title: str | None = '60 минут'
    description: str | None = 'Таймер на 60 минут'

    def perform(self):
        TimerService().add_duration_timer(timedelta(minutes=60))
        ToastService().add(f'Таймер установлен на 60 минут')

        
class TimerDialogAction(BaseAction):
    group: str = 'TIME'
    order: int = 2

    icon_path: str | None = 'icons8-timer-50.png'
    title: str | None = 'Добавить тайме'
    description: str | None = 'Добавить таймеm'

    def perform(self):
        dialog = TimerDialog(self.parent().window())
        dialog.exec()

        
class TimersListAction(BaseAction):
    group: str = 'TIME'
    order: int = 2

    icon_path: str | None = 'icons8-bulleted-list-100.png'
    title: str | None = 'Список таймеров'
    description: str | None = 'Список таймеров'

    def perform(self):
        dialog = TimersListDialog(self.parent().window())
        dialog.exec()