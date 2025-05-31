import os
from PyQt6.QtWidgets import QFileDialog
from app.config import configs

class FileDialog(QFileDialog):
    @staticmethod
    def getOpenFileNamesEx(parent = None, caption = None, filter = None):

        dialog = QFileDialog(parent)
        dialog.setWindowTitle(caption)
        dialog.setNameFilter(filter)
        dialog.setDirectory(configs.LAST_USED_FOLDER_OPEN)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        
        if dialog.exec():
            files = dialog.selectedFiles()
            if files:
                configs.LAST_USED_FOLDER_OPEN = os.path.dirname(files[0])
            return files
        return []

    @staticmethod
    def getSaveFileNameEx(parent = None, caption = None, filter = None, default_extension=None):
        dialog = QFileDialog(parent)
        dialog.setWindowTitle(caption)
        dialog.setNameFilter(filter)
        dialog.setDirectory(configs.LAST_USED_FOLDER_SAVE)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setDefaultSuffix(default_extension)
        
        if dialog.exec():
            file = dialog.selectedFiles()[0]
            if file:
                configs.LAST_USED_FOLDER_SAVE = os.path.dirname(file)
            return file
        return None
