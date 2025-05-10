import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import logging
import tempfile
from PIL import ImageGrab, Image
from PyQt6.QtGui import QGuiApplication, QClipboard
from PyQt6.QtCore import QRect

class OCRService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def capture_and_recognize(self, rect: QRect = None):
        try:
            if rect is None:
                screenshot = ImageGrab.grab()
            else:
                screenshot = ImageGrab.grab(bbox=(
                    rect.x(), rect.y(), 
                    rect.x() + rect.width(), 
                    rect.y() + rect.height()
                ))

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                screenshot.save(temp_file.name)
                logging.debug(f"Screenshot saved to {temp_file.name}")

            text = pytesseract.image_to_string(screenshot, lang='rus+eng')
            text = text.strip()

            if text:
                clipboard = QGuiApplication.clipboard()
                clipboard.setText(text)
                return True

            return False
        except Exception as e:
            logging.error(f"OCR error: {e}")
            return False