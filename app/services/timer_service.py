import logging
import winsound
from datetime import datetime, timedelta
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from app.core.config import configs


class TimerItem(QObject):
    expire = pyqtSignal()

    def __init__(self, end_time, desc=''):
        super().__init__()
        self.end_time = end_time
        self.desc = desc
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._expire)
        self.timer.start(int(self.remaining_time.total_seconds() * 1000))

    @property
    def remaining_time(self) -> timedelta:
        return self.end_time - datetime.now()

    def _expire(self):
        self.expire.emit()
        
    def cancel(self):
        self.timer.stop()


class TimerService(QObject):
    timer_added = pyqtSignal(TimerItem)
    timer_finished = pyqtSignal(TimerItem)
    timer_removed = pyqtSignal(str)

    _instance = None

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

        self.timers = {}

    def add_timer(self, end_time: datetime, disc='') -> TimerItem:
        timer_id = str(len(self.timers)) + end_time.isoformat()
        timer_item = TimerItem(end_time, disc)
        
        self.timers[timer_id] = timer_item
        self.timer_added.emit(timer_item)
        
        timer_item.expire.connect(self._timer_finished)
        
        return timer_item

    def add_duration_timer(self, duration: timedelta, disc='') -> TimerItem:
        return self.add_timer(datetime.now() + duration, disc)

    def remove_timer(self, timer_id: str):
        if timer_id in self.timers:
            timer_item = self.timers[timer_id]
            timer_item.cancel()
            del self.timers[timer_id]
            self.timer_removed.emit(timer_id)

    def _timer_finished(self, timer_id: str):
        if timer_id in self.timers:
            timer_item = self.timers[timer_id]
            self._play_notification()
            self.timer_finished.emit(timer_item)
            self.remove_timer(timer_id)

    def _play_notification(self):
        try:
            winsound.PlaySound(configs.NOTIFICATION_SOUND_PATH, winsound.SND_FILENAME)
        except Exception as e:
            logging.error(f"Error playing notification sound: {e}")