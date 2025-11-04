
import re
import logging
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QGuiApplication
from app.core.base_action import BaseAction
from app.views.dialogs.lines_dialog import QLinesInputDialog
from app.services.integration_service import IntegrationService, TelegramSendMessageNotebookBot
from app.services.toast_service import ToastService


class LayoutSwitchAction(BaseAction):
    group: str = 'TEXT'
    order: int = 1

    icon_path: str | None = 'icons8-switch-50.png'
    title: str | None = 'RU/EN'
    description: str | None = 'Переключить раскладку RU/EN'
    en_to_ru = {
        '`': 'ё', '~': 'Ё', '!': '!', '@': '"', '#': '№', '$': ';', '%': '%',
        '^': ':', '&': '?', 'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е',
        'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ',
        'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о',
        'k': 'л', 'l': 'д', ';': 'ж', "'": 'э', 'z': 'я', 'x': 'ч', 'c': 'с',
        'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю', '/': '.',
        'Q': 'Й', 'W': 'Ц', 'E': 'У', 'R': 'К', 'T': 'Е', 'Y': 'Н', 'U': 'Г',
        'I': 'Ш', 'O': 'Щ', 'P': 'З', '{': 'Х', '}': 'Ъ', 'A': 'Ф', 'S': 'Ы',
        'D': 'В', 'F': 'А', 'G': 'П', 'H': 'Р', 'J': 'О', 'K': 'Л', 'L': 'Д',
        ':': 'Ж', '"': 'Э', '|': '/', 'Z': 'Я', 'X': 'Ч', 'C': 'С', 'V': 'М',
        'B': 'И', 'N': 'Т', 'M': 'Ь', '<': 'Б', '>': 'Ю', '?': ','
    }
    ru_to_en = {v: k for k, v in en_to_ru.items()}

    def perform(self):
        
        try:
            clipboard = QGuiApplication.clipboard()
            text = clipboard.text()
        
            if not text:
                ToastService().add('Буфер обмена пуст')
                return
            
            if any(c in self.en_to_ru for c in text):
                translated = ''.join([self.en_to_ru.get(c, c) for c in text])
            else:
                translated = ''.join([self.ru_to_en.get(c, c) for c in text])
        
            clipboard.setText(translated)
            ToastService().add('Раскладка клавиатуры изменена')
        except Exception as exc:
            logging.error(f"Ошибка преобразования текста: {exc}")


class TelegramAction(BaseAction):
    group: str = 'TEXT'
    order: int = 3

    icon_path: str | None = 'icons8-telegram-50.png'
    title: str | None = 'Telegram Заметки'
    description: str | None = 'Отправить заметку в Telegram'

    def perform(self):
        try:
            dialog = QLinesInputDialog(self.parent().window())
        
            if dialog.exec() == QDialog.DialogCode.Accepted:
                text = dialog.toPlainText()
                if text:
                    task = TelegramSendMessageNotebookBot(text)
                    task.request_finished.connect(self._on_sended)
                    task.request_error.connect(self._on_error)
                    IntegrationService().run_task(task)

        except Exception as exc:
            logging.error(f"Ошибка преобразования текста: {exc}")

    def _on_sended(self, data):
        ToastService().add("Сообщение отправлено Telegram")

    def _on_error(self, data):
        ToastService().add("Не удалось отправить сообщение Telegram")
            


class AITextConvertAction(BaseAction):
    group: str = 'TEXT'
    order: int = 2

    icon_path: str | None = 'icons8-text-color-48.png'
    title: str | None = 'Очистить AI текс'
    description: str | None = 'Автозамена спецсимволов AI текста'

    allowed_pattern = re.compile(r'[^a-zA-Zа-яА-ЯёЁ0-9 .,!?;:\-()\[\]{}<>@#$%^&*_+=\\/\\|\'"«»\n]')

    def perform(self):

        try:
            clipboard = QGuiApplication.clipboard()
            text = clipboard.text()
            
            if not text:
                ToastService().add('Буфер обмена пуст')
                return
            
            cleaned_text = self.allowed_pattern.sub(' ', text)
            cleaned_text = re.sub(' +', ' ', cleaned_text)
            
            if cleaned_text != text:
                clipboard.setText(cleaned_text)
                ToastService().add(f"Текст изменен")
            else:
                ToastService().add("Текст не содержит недопустимых символов")
                
        except Exception as exc:
            logging.error(f"Ошибка преобразования текста: {exc}")
