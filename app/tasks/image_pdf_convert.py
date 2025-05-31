import os
from PIL import Image
from fpdf import FPDF
from PyQt6.QtCore import QThread, pyqtSignal


class PdfConverterThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, image_paths):
        super().__init__()
        self.image_paths = image_paths
        self.margin = 0

    def run(self):
        try:
            pdf_object = FPDF()
            
            for image_path in self.image_paths:
                try:
                    with Image.open(image_path) as img:
                        if img.mode in ('RGBA', 'P'):
                            img = img.convert('RGB')
                        
                        width, height = img.size
                        
                        if width > height:
                            pdf_object.add_page(orientation='L')
                            pdf_width = pdf_object.w - 2 * self.margin
                            pdf_height = (height / width) * pdf_width
                            if pdf_height > pdf_object.h - 2 * self.margin:
                                pdf_height = pdf_object.h - 2 * self.margin
                                pdf_width = (width / height) * pdf_height
                        else:
                            pdf_object.add_page(orientation='P')
                            pdf_height = pdf_object.h - 2 * self.margin
                            pdf_width = (width / height) * pdf_height
                            if pdf_width > pdf_object.w - 2 * self.margin:
                                pdf_width = pdf_object.w - 2 * self.margin
                                pdf_height = (height / width) * pdf_width
                        
                        x = (pdf_object.w - pdf_width) / 2
                        y = (pdf_object.h - pdf_height) / 2

                        pdf_object.image(img, x=x, y=y, w=pdf_width, h=pdf_height)
                        
                        self.progress.emit(f"Файл обработан: {os.path.basename(image_path)}")
                
                except Exception as e:
                    self.error.emit(f"Ошибка при обработке {os.path.basename(image_path)}: {str(e)}")
            
            self.finished.emit(pdf_object)
        
        except Exception as e:
            self.error.emit(f"Критическая ошибка при создании PDF: {str(e)}")