import os
from PIL import Image
from fpdf import FPDF
from app.services.toast_service import ToastService
from app.tasks.image_pdf_convert import PdfConverterThread
from app.tasks.pdf_merge import PdfMergerThread
from app.views.dialogs.files_dialog import FileDialog
from app.views.qelements import QIconButton

class PdfConvertButton(QIconButton):
    def __init__(self):
        super().__init__("icons8-pdf-50.png", "Конвертировать изображения в PDF")
        
    def on_click(self):
        try:
            image_paths = FileDialog.getOpenFileNamesEx(self.window(), None, "Images (*.png *.jpg *.jpeg *.bmp)")

            if not image_paths:
                ToastService().add("Не выбрано ни одного изображения")
                return
                                
            self.converter = PdfConverterThread(image_paths)
            self.converter.progress.connect(lambda msg: ToastService().add(msg))
            self.converter.error.connect(lambda msg: ToastService().add(msg))
            self.converter.finished.connect(self.on_pdf_ready)
            self.converter.start()
                
        except Exception as e:
            ToastService().add(f"Ошибка при создании PDF: {str(e)}")

    def on_pdf_ready(self, pdf_object):
        try:
            pdf_path = FileDialog.getSaveFileNameEx(self.window(), "Сохранить PDF как", "PDF Files (*.pdf)")
            
            if not pdf_path:
                return
            
            if not pdf_path.lower().endswith('.pdf'):
                pdf_path += '.pdf'
            
            pdf_object.output(pdf_path)
            ToastService().add(f"PDF успешно создан: {os.path.basename(pdf_path)}")
            os.startfile(pdf_path)
            
        except Exception as e:
            ToastService().add(f"Ошибка при сохранении PDF: {str(e)}")


class MergePdfButton(QIconButton):
    def __init__(self):
        super().__init__("icons8-merge-50.png", "Объединить PDF файлы")
        
    def on_click(self):
        try:
            pdf_paths = FileDialog.getOpenFileNamesEx(self.window(), None, "PDF Files (*.pdf)")
                
            if len(pdf_paths) < 2:
                ToastService().add("Выберите хотя бы 2 PDF файла для объединения")
                return
                
            self.merger = PdfMergerThread(pdf_paths)
            self.merger.progress.connect(lambda msg: ToastService().add(msg))
            self.merger.error.connect(lambda msg: ToastService().add(msg))
            self.merger.finished.connect(self.on_pdf_ready)
            self.merger.start()
                
        except Exception as e:
            ToastService().add(f"Ошибка при создании PDF: {str(e)}")

    def on_pdf_ready(self, pdf_object):
        try:
            pdf_path = FileDialog.getSaveFileNameEx(self.window(), "Сохранить PDF как", "PDF Files (*.pdf)")
            
            if not pdf_path:
                return
            
            if not pdf_path.lower().endswith('.pdf'):
                pdf_path += '.pdf'
            
            pdf_object.write(pdf_path)
            ToastService().add(f"PDF успешно создан: {os.path.basename(pdf_path)}")
            os.startfile(pdf_path)
            
        except Exception as e:
            ToastService().add(f"Ошибка при сохранении PDF: {str(e)}")



