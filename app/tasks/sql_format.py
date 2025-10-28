import sqlparse
from sqlparse.tokens import Keyword, Name, Punctuation, Wildcard, Comment
from sqlparse.sql import Identifier, IdentifierList, Parenthesis
from PyQt6.QtCore import QThread, pyqtSignal


class SqlFormatThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        try:
            formatted_sql = sqlparse.format(self.text, reindent=True, keyword_case='upper')
            
            self.finished.emit(formatted_sql)
        
        except Exception as e:
            self.error.emit(f"Ошибка при форматировании SQL: {str(e)}")