import os
import sys
import ctypes
import subprocess
from PyQt6.QtGui import QGuiApplication
from app.core.base_action import BaseAction
from app.services.toast_service import ToastService
from app.core.config import configs

class IPClientRunAction(BaseAction):
    group: str = 'IPCLIENT'
    order: int = 7

    icon_path: str | None = 'icons8-vpn-100.png'
    title: str | None = 'IP-Client'
    description: str | None = 'Запустить IP-Client'

    def perform(self):
        try:
            ipclient_script = os.path.join(configs.SCRIPTS_DIR, 'ipclient.py')
            ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, f'"{ipclient_script}" "{configs.PROJECT_ROOT}" on', None, 1)
            QGuiApplication.clipboard().setText(configs.IPCLIENT_PIN)
            ToastService().add(f"Дождитесь запуска, пин код уже в вашем буфере обмена")
        except Exception as e:
            ToastService().add(f"Ошибка запуска IP-Client: {e}")

    @classmethod
    def is_available(cls):
        if not configs.IPCLIENT_EXE:
            return False
            
        if not os.path.isfile(configs.IPCLIENT_EXE):
            return False
            
        return True

class IPClientStopAction(BaseAction):
    group: str = 'IPCLIENT'
    order: int = 8

    icon_path: str | None = 'icons8-off-91.png'
    title: str | None = 'Остановить IP-Client'
    description: str | None = 'Остановить IP-Client и связанные службы'

    def perform(self):
        try:
            ipclient_script = os.path.join(configs.SCRIPTS_DIR, 'ipclient.py')
            r = ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, f'"{ipclient_script}" "{configs.PROJECT_ROOT}" off', None, 1)
        except Exception as e:
            ToastService().add(f"Ошибка остановки IP-Client: {e}")

    @classmethod
    def is_available(cls):
        if not configs.IPCLIENT_EXE:
            return False
            
        if not os.path.isfile(configs.IPCLIENT_EXE):
            return False
            
        return True
