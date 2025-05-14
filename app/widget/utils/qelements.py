from PyQt6.QtWidgets import QFrame, QDialog, QLabel, QTextEdit, QDialogButtonBox, QVBoxLayout
from PyQt6.QtCore import Qt, QEvent


class QSeparator(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setFixedHeight(1)


class QLinesInputBox(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Dialog
        )
        self.setGeometry(parent.geometry())
        
        parent.installEventFilter(self)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        self.text_edit = QTextEdit()

        layout.addWidget(self.text_edit)
        
        button_box = QDialogButtonBox()
        
        self.btn_ok = button_box.addButton("Отправить", QDialogButtonBox.ButtonRole.AcceptRole)
        self.btn_ok.setObjectName('okButton')
        self.btn_cancel = button_box.addButton("Отмена", QDialogButtonBox.ButtonRole.RejectRole)
        self.btn_cancel.setObjectName('cancelButton')
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Hide:
            self.reject()
        return super().eventFilter(obj, event)

    def toPlainText(self):
        return self.text_edit.toPlainText()