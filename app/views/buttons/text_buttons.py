
import re
import logging
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QGuiApplication
from app.views.qelements import QIconButton
from app.views.dialogs.lines_dialog import QLinesInputDialog
from app.services.telegram_service import TelegramService
from app.services.toast_service import ToastService
from app.config import configs


class LayoutSwitchButton(QIconButton):
    def __init__(self):
        super().__init__("icons8-switch-50.png", "Переключить раскладку RU/EN")

        self.en_to_ru = {
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
        self.ru_to_en = {v: k for k, v in self.en_to_ru.items()}
        
    def on_click(self):
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
        except:
            logging.error(f"Ошибка преобразования текста: {e}")


class TelegramButton(QIconButton):
    def __init__(self):
        super().__init__("icons8-telegram-50.png", "Отправить заметку в Telegram")

    def on_click(self):
        dialog = QLinesInputDialog(self.window())
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            text = dialog.toPlainText()
            if text:
                if TelegramService().send_message(text):
                    ToastService().add("Сообщение отправлено Telegram")
                else:
                    ToastService().add("Не удалось отправить сообщение Telegram")


class AITextConvertButton(QIconButton):
    def __init__(self):
        super().__init__("icons8-text-color-48.png", "Автозамена спецсимволов AI текста")

        self.allowed_pattern = re.compile(r'[^a-zA-Zа-яА-ЯёЁ0-9 .,!?;:\-()\[\]{}<>@#$%^&*_+=\\/\\|\'"«»\n]')

    def on_click(self):
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
                
        except Exception as e:
            logging.error(f"Ошибка преобразования текста: {e}")
