import os
from PyPDF2 import PdfMerger
from PyQt6.QtCore import QThread, pyqtSignal


class PdfMergerThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, pdf_paths):
        super().__init__()
        self.pdf_paths = pdf_paths

    def run(self):
        try:
            merger = PdfMerger()
                    
            for pdf_path in self.pdf_paths:
                merger.append(pdf_path)
                self.progress.emit(f"Файл обработан: {os.path.basename(pdf_path)}")
                
            self.finished.emit(merger)
        
        except Exception as e:
            self.error.emit(f"Критическая ошибка при создании PDF: {str(e)}")