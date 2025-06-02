import logging
from PyQt6.QtWidgets import QWidget, QFrame, QDialog, QLabel, QTextEdit, QDialogButtonBox, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, QEvent, pyqtSignal, QTimer
from app.util.qelements import QDialogParentHide


class QLinesInputDialog(QDialogParentHide):
    def __init__(self, parent):
        super().__init__(parent)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        self.text_edit = QTextEdit()

        layout.addWidget(self.text_edit)
        
        button_box = QDialogButtonBox()
        
        self.btn_ok = button_box.addButton("Отправить", QDialogButtonBox.ButtonRole.AcceptRole)
        self.btn_cancel = button_box.addButton("Отмена", QDialogButtonBox.ButtonRole.RejectRole)
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)

    def toPlainText(self):
        return self.text_edit.toPlainText()