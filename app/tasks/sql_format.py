import sqlparse
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
            formatted_sql = sqlparse.format(
                self.text,
                keyword_case='upper',
                identifier_case=None,
                strip_comments=True,
                truncate_strings=None,
                truncate_char=None,
                reindent=True,
                reindent_aligned =True,
                use_space_around_operators=True,
                indent_tabs=False,
                indent_width=4,
                wrap_after=5000,
                compact=False,
                output_format=None,
                comma_first=False,
            )
            
            self.finished.emit(formatted_sql)
        
        except Exception as e:
            self.error.emit(f"Ошибка при форматировании SQL: {str(e)}")