import os
import sys
import psutil
import subprocess
import win32service
import win32serviceutil


def start_ipclient():
    # Запуск приложения
    subprocess.Popen([configs.IPCLIENT_EXE])
        
    # Запуск службы Windows
    win32serviceutil.StartService(configs.IPCLIENT_SERVICE_NAME)


def stop_ipclient():
    # Гасим ошибки специально как хуйня

    # Остановка приложения
    process_name = os.path.basename(configs.IPCLIENT_EXE)
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
            try:
                try:
                    proc.terminate()
                    proc.wait(timeout=5)
                except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                    try:
                        proc.kill()
                    except psutil.NoSuchProcess:
                        pass
            except:
                pass
        
    # Остановка службы Windows
    try:
        win32serviceutil.StopService(configs.IPCLIENT_SERVICE_NAME)
    except:
        pass



if __name__ == "__main__":
    project_root = sys.argv[1]
    action = sys.argv[2].lower()

    sys.path.append(project_root)
    from app.core.config import configs

    
    if action == "on":
        start_ipclient()
    elif action == "off":
        stop_ipclient()
    else:
        print("Неизвестная команда. Используйте 'on' или 'off'")
        sys.exit(1)


