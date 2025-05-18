
import logging
from PyQt6.QtWidgets import QFrame, QLabel, QGridLayout
from PyQt6.QtCore import Qt, QTimer, QDateTime, QLocale
from app.core.config import configs

class DateTimeView(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("DateTimeView")
        
        self.locale = QLocale()
        self.layout = QGridLayout()    
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        self.time_label = QLabel()
        self.time_label.setObjectName("TimeLabel")
        self.layout.addWidget(self.time_label, 0, 0)

        self.date_label = QLabel()
        self.date_label.setObjectName("DateLabel")
        self.layout.addWidget(self.date_label, 1, 0)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        
    def start(self):
        self.update_time()
        self.timer.start(configs.TIME_INTERVAL_UPDATE)

    def stop(self):
        self.timer.stop()

    def update_time(self):
        current_time = QDateTime.currentDateTime()

        fulltime_str = self.locale.toString(current_time, configs.DATETIME_FORMAT)
        time_str = self.locale.toString(current_time, configs.TIME_FORMAT)
        date_str = self.locale.toString(current_time, configs.DATEFULL_FORMAT)

        logging.debug(f"Time event {fulltime_str}")
        
        self.time_label.setText(time_str)                
        self.date_label.setText(date_str)        