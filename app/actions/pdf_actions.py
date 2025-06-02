import os
from app.core.base_action import BaseAction
from app.services.toast_service import ToastService
from app.tasks.image_pdf_convert import PdfConverterThread
from app.tasks.pdf_merge import PdfMergerThread
from app.views.dialogs.files_dialog import FileDialog

class JPG2PDFConvertAction(BaseAction):
    group: str = 'PDF'
    order: int = 1

    icon_path: str | None = 'icons8-pdf-50.png'
    title: str | None = 'Конвертировать изображения в PDF'
    description: str | None = 'Конвертировать изображения в PDF'

    def perform(self):
        try:
            image_paths = FileDialog.getOpenFileNamesEx(self.parent().window(), None, "Images (*.png *.jpg *.jpeg *.bmp)")

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
            pdf_path = FileDialog.getSaveFileNameEx(self.parent().window(), "Сохранить PDF как", "PDF Files (*.pdf)")
            
            if not pdf_path:
                return
            
            if not pdf_path.lower().endswith('.pdf'):
                pdf_path += '.pdf'
            
            pdf_object.output(pdf_path)
            ToastService().add(f"PDF успешно создан: {os.path.basename(pdf_path)}")
            os.startfile(pdf_path)
            
        except Exception as e:
            ToastService().add(f"Ошибка при сохранении PDF: {str(e)}")


class MergePdfAction(BaseAction):
    group: str = 'PDF'
    order: int = 2

    icon_path: str | None = 'icons8-merge-50.png'
    title: str | None = 'Объединить PDF файлы'
    description: str | None = 'Объединить PDF файлы'

    def perform(self):
        try:
            pdf_paths = FileDialog.getOpenFileNamesEx(self.parent().window(), None, "PDF Files (*.pdf)")
                
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
            pdf_path = FileDialog.getSaveFileNameEx(self.parent().window(), "Сохранить PDF как", "PDF Files (*.pdf)")
            
            if not pdf_path:
                return
            
            if not pdf_path.lower().endswith('.pdf'):
                pdf_path += '.pdf'
            
            pdf_object.write(pdf_path)
            ToastService().add(f"PDF успешно создан: {os.path.basename(pdf_path)}")
            os.startfile(pdf_path)
            
        except Exception as e:
            ToastService().add(f"Ошибка при сохранении PDF: {str(e)}")



