
import logging
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QTimer, QDateTime
from PyQt6.QtCore import QLocale
from app.core.config import configs

class DateTimeView(QLabel):
    def __init__(self):
        super().__init__()
        self.locale = QLocale()
        self.update_time()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(configs.TIME_INTERVAL_UPDATE)

    def update_time(self):
        current_time = QDateTime.currentDateTime()
        time_str = self.locale.toString(current_time, configs.DATETIME_FORMAT)
        logging.debug(f"Time event {time_str}")
        
        self.setText(time_str)        
        self.setToolTip(self.locale.toString(current_time, configs.DATETIMEFULL_FORMAT))