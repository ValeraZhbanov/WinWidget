
from PyQt6.QtWidgets import QPushButton, QHBoxLayout
from PyQt6.QtGui import QGuiApplication, QClipboard, QIcon
from app.widget.views.buttons.base_button import BaseButton
from app.core.config import configs


class LayoutSwitchButton(BaseButton):
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
                return
            
            if any(c in self.en_to_ru for c in text):
                translated = ''.join([self.en_to_ru.get(c, c) for c in text])
            else:
                translated = ''.join([self.ru_to_en.get(c, c) for c in text])
        
            clipboard.setText(translated)
        except:
            logging.error(f"Ошибка преобразования текста в браузере: {e}")