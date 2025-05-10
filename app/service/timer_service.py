import logging
import winsound
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from app.core.config import configs

class TimerService(QObject):
    timer_finished = pyqtSignal(str)
    timer_updated = pyqtSignal(str)

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

        self.timer = QTimer()
        self.timer.timeout.connect(self._update_timer)
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.is_running = False

    def start_timer(self, seconds: int):
        self.total_seconds = seconds
        self.remaining_seconds = seconds
        self.is_running = True
        self.timer.start(1000)
        self.timer_updated.emit(self._format_time())

    def stop_timer(self):
        self.timer.stop()
        self.is_running = False
        self.remaining_seconds = 0

    def _update_timer(self):
        self.remaining_seconds -= 1
        self.timer_updated.emit(self._format_time())

        if self.remaining_seconds <= 0:
            self.timer.stop()
            self.is_running = False
            self._play_notification()
            self.timer_finished.emit("Timer finished!")

    def _format_time(self) -> str:
        minutes, seconds = divmod(self.remaining_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def _play_notification(self):
        try:
            winsound.PlaySound(configs.NOTIFICATION_SOUND_PATH, winsound.SND_FILENAME)
        except Exception as e:
            logging.error(f"Error playing notification sound: {e}")