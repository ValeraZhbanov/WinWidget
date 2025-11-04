
from datetime import timedelta
from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QGridLayout, QPushButton, QDateTimeEdit, QTimeEdit, QPlainTextEdit, QListWidget, QAbstractItemView, QDialogButtonBox
from PyQt6.QtCore import Qt, pyqtSignal, QDateTime
from app.util.qelements import QDialogParentHide
from app.services.timer_service import TimerService
from app.services.toast_service import ToastService
from app.core.config import configs


class QTimerDialog(QDialogParentHide):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить таймер")
        
        layout = QVBoxLayout()
        
        self.tab_widget = QTabWidget()
        
        duration_tab = QWidget()
        duration_layout = QVBoxLayout()
        duration_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.quick_buttons_layout = QGridLayout()

        quick_buttons = [
            [(10, "10 мин"), (20, "20 мин"), (30, "30 мин"),],
            [(60, "1 час"), (90, "1.5 часа"), (120, "2 часа"),],
        ]

        for row_it, row in enumerate(quick_buttons):
            for col_it, (minutes, text) in enumerate(row):
                btn = QPushButton(text)
                btn.setObjectName('QuickTimerButton')
                btn.clicked.connect(lambda _, m=minutes: self._add_duration_timer(m * 60))
                self.quick_buttons_layout.addWidget(btn, row_it, col_it)
            
        duration_layout.addLayout(self.quick_buttons_layout)
        
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat(configs.TIME_FORMAT)
        duration_layout.addWidget(self.time_edit)

        self.timetext_edit = QPlainTextEdit()
        duration_layout.addWidget(self.timetext_edit)

        duration_layout.addStretch(1)
        
        button_box = QDialogButtonBox()

        add_duration_btn = button_box.addButton("Добавить таймер", QDialogButtonBox.ButtonRole.ActionRole)
        add_duration_btn.clicked.connect(self._add_custom_duration_timer)

        button_box.addButton("Закрыть", QDialogButtonBox.ButtonRole.RejectRole)
        button_box.rejected.connect(self.reject)

        duration_layout.addWidget(button_box)
        
        duration_tab.setLayout(duration_layout)
        
        datetime_tab = QWidget()
        datetime_layout = QVBoxLayout()
        
        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        self.datetime_edit.setDisplayFormat(configs.DATETIME_FORMAT)
        datetime_layout.addWidget(self.datetime_edit)

        self.datetimetext_edit = QPlainTextEdit()
        datetime_layout.addWidget(self.datetimetext_edit)

        datetime_layout.addStretch(1)

        button_box = QDialogButtonBox()

        add_datetime_btn = button_box.addButton("Добавить таймер", QDialogButtonBox.ButtonRole.ActionRole)
        add_datetime_btn.clicked.connect(self._add_datetime_timer)

        button_box.addButton("Закрыть", QDialogButtonBox.ButtonRole.RejectRole)
        button_box.rejected.connect(self.reject)

        datetime_layout.addWidget(button_box)
        
        datetime_tab.setLayout(datetime_layout)
        
        self.tab_widget.addTab(duration_tab, "По длительности")
        self.tab_widget.addTab(datetime_tab, "По времени")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        
    def _add_duration_timer(self, seconds):
        disc = self.timetext_edit.toPlainText()
        TimerService().add_duration_timer(timedelta(seconds=seconds), disc)
        ToastService().add(f"Таймер добавлен на {seconds // 60} минут")
        self.accept()
        
    def _add_custom_duration_timer(self):
        time = self.time_edit.time()
        
        seconds = time.hour() * 3600 + time.minute() * 60 + time.second()
        if seconds > 0:
            self._add_duration_timer(seconds)
            
    def _add_datetime_timer(self):
        datetime = self.datetime_edit.dateTime().toPyDateTime()
        disc = self.datetimetext_edit.toPlainText()
        if datetime > datetime.now():
            TimerService().add_timer(datetime, disc)
            ToastService().add(f"Таймер добавлен на {datetime.strftime('%d.%m.%Y %H:%M')}")
            self.accept()


class QTimersListDialog(QDialogParentHide):
    timer_removed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Активные таймеры")
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.timers_list = QListWidget()
        self.timers_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        layout.addWidget(self.timers_list)

        layout.addStretch(1)

        button_box = QDialogButtonBox()

        remove_btn = button_box.addButton("Удалить выбранный", QDialogButtonBox.ButtonRole.ActionRole)
        remove_btn.clicked.connect(self._remove_selected_timer)

        button_box.addButton("Закрыть", QDialogButtonBox.ButtonRole.RejectRole)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        
        self.update_timers_list()
        TimerService().timer_added.connect(self.update_timers_list)
        TimerService().timer_removed.connect(self.update_timers_list)
        
        self.setLayout(layout)
        
    def update_timers_list(self):
        self.timers_list.clear()
        for id, timer in TimerService().timers.items():
            item_text = f"{timer.end_time.strftime('%d.%m.%Y %H:%M')} - {timer.desc or 'Таймер'}"
            self.timers_list.addItem(item_text)
            self.timers_list.item(self.timers_list.count() - 1).setData(Qt.ItemDataRole.UserRole, id)
            
    def _remove_selected_timer(self):
        selected = self.timers_list.currentItem()
        if selected:
            timer_id = selected.data(Qt.ItemDataRole.UserRole)
            TimerService().remove_timer(timer_id)