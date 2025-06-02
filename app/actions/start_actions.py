
import os
import ctypes
import subprocess
import subprocess
from app.core.base_action import BaseAction
from app.services.toast_service import ToastService
from app.core.config import configs


class NotepadRunAction(BaseAction):
    group: str = 'START'
    order: int = 1

    icon_path: str | None = 'icons8-notepad-50.png'
    title: str | None = 'Блокнот'
    description: str | None = 'Запустить блокнот'

    def perform(self):
        try:
            subprocess.Popen(['notepad.exe'])
        except Exception as e:
            ToastService().add(f"Ошибка запуска блокнота: {e}")

    def is_available():
        try:
            subprocess.run(['where', 'notepad.exe'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False


class CmdRunAction(BaseAction):
    group: str = 'START'
    order: int = 2

    icon_path: str | None = 'icons8-pdf-50.png'
    title: str | None = 'Консоль'
    description: str | None = 'Запустить консоль'

    def perform(self):
        try:
            user_profile = os.path.expanduser('~')
            ctypes.windll.shell32.ShellExecuteW(None, None, 'cmd.exe', f'/K "cd /d {user_profile}"', user_profile, 1)
        except Exception as e:
            ToastService().add(f"Ошибка запуска командной строки: {e}")

    def is_available():
        try:
            subprocess.run(['where', 'cmd.exe'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False


class CmdAdminRunAction(CmdRunAction):
    group: str = 'START'
    order: int = 3

    icon_path: str | None = 'icons8-cmd-80.png'
    title: str | None = 'Консоль администратора'
    description: str | None = 'Запустить консоль администратора'

    def perform(self):
        try:
            user_profile = os.path.expanduser('~')
            ctypes.windll.shell32.ShellExecuteW(None, 'runas', 'cmd.exe', f'/K "cd /d {user_profile}"', user_profile, 1)
        except Exception as e:
            ToastService().add(f"Ошибка запуска командной строки от имени администратора: {e}")


class ZapretButton(BaseAction):
    group: str = 'START'
    order: int = 4

    icon_path: str | None = 'icons8-hack-64.png'
    title: str | None = 'Zapret'
    description: str | None = 'Запустить файл настройки утилиты Zapret'

    def perform(self):
        try:
            ctypes.windll.shell32.ShellExecuteW(None, 'runas', configs.ZAPRET_SERVICE_BAT, None, None, 1)
        except Exception as e:
            ToastService().add(f"Ошибка запуска zapret-service.bat от имени администратора: {e}")

    def is_available():
        if not configs.ZAPRET_SERVICE_BAT:
            return False
            
        if not os.path.isfile(configs.ZAPRET_SERVICE_BAT):
            return False
            
        return True


