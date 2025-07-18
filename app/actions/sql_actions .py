
from pydoc import importfile
import re
import logging
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QGuiApplication
from app.core.base_action import BaseAction
from app.tasks.sql_format import SqlFormatThread
from app.services.toast_service import ToastService


class SqlFormatAction(BaseAction):
    group: str = 'SQL'
    order: int = 3

    icon_path: str | None = 'icons8-sql-50.png'
    title: str | None = 'SQL форматирование'
    description: str | None = 'Форматировать SQL запрос'

    def perform(self):
        try:
            text = QGuiApplication.clipboard().text()
            
            if not text:
                ToastService().add('Буфер обмена пуст')
                return
            
            self.formated = SqlFormatThread(text)
            self.formated.error.connect(lambda msg: ToastService().add(msg))
            self.formated.finished.connect(self._on_formated)
            self.formated.start()
            
        except Exception as exc:
            logging.error(f"Ошибка преобразования текста: {exc}")

    def _on_formated(self, text):
        QGuiApplication.clipboard().setText(text)
        ToastService().add(f"Форматирование завершено")

