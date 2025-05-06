@echo off
setlocal EnableDelayedExpansion
chcp 65001 > nul
:: 65001 - UTF-8

:: Admin rights check
if "%1"=="admin" (
    echo Started with admin rights
) else (
    echo Requesting admin rights...
    powershell -Command "Start-Process 'cmd.exe' -ArgumentList '/c \"\"%~f0\" admin\"' -Verb RunAs"
    exit /b
)

set "SCRIPT_PATH=%~dp0..\service.pyw"
set "PYTHON_LIBS_PATH=%~dp0..\requirements.txt"
set "TASK_NAME=WinWidgetTask"
set "PROCESS_NAME=python.exe"
set "APP_TITLE=WinWidget"  :: Change this to your application window title
set "PYTHONW_PATH="

:: 1. Поиск через where (если есть в PATH)
where pythonw.exe >nul 2>&1
if %errorlevel% equ 0 (
    for /f "delims=" %%i in ('where pythonw.exe') do (
        set "PYTHONW_PATH=%%i"
        goto admin_check
    )
)

:: 2. Проверка стандартных путей
for %%d in (
    "%LOCALAPPDATA%\Programs\Python\Python311\pythonw.exe",
    "%LOCALAPPDATA%\Programs\Python\Python310\pythonw.exe",
    "%APPDATA%\Python\Python311\pythonw.exe",
    "C:\Python311\pythonw.exe",
    "C:\Python310\pythonw.exe"
) do (
    if exist "%%~d" (
        set "PYTHONW_PATH=%%~d"
        goto admin_check
    )
)

echo Python not found automatically.
set /p PYTHONW_PATH="Enter full path to pythonw.exe: "
if not exist "!PYTHONW_PATH!" (
    echo Invalid path provided
    pause
    exit /b 1
)

:admin_check

echo %PYTHONW_PATH%

:: Kill existing processes
echo Checking for running instances...
tasklist /FI "IMAGENAME eq %PROCESS_NAME%" 2>nul | find /i "%PROCESS_NAME%" >nul

if %errorlevel% == 0 (
    echo Terminating existing processes...
    
    :: First try graceful termination
    taskkill /IM "%PROCESS_NAME%" /T /FI "WINDOWTITLE eq %SCRIPT_PATH%" >nul 2>&1
    timeout /t 3 /nobreak >nul
    
    :: Force kill if still running
    tasklist /FI "IMAGENAME eq %PROCESS_NAME%" 2>nul | find /i "%PROCESS_NAME%" >nul
    if %errorlevel% == 0 (
        taskkill /F /IM "%PROCESS_NAME%" /T >nul 2>&1
        echo Forcefully terminated all instances.
    ) else (
        echo Successfully closed running instances.
    )
)

:: Remove existing task if exists
echo Removing existing scheduled task...
schtasks /delete /tn "%TASK_NAME%" /f 2>nul

pip install -U -r "%PYTHON_LIBS_PATH%"

:: Create new task
echo Creating new scheduled task...
schtasks /create /tn "%TASK_NAME%" /tr "%PYTHONW_PATH% \"%SCRIPT_PATH%\"" /sc onlogon /it /ru %USERNAME% /rl highest

if %errorlevel% neq 0 (
    echo ERROR: Failed to create task!
    pause
    exit /b
)

:: Run task immediately
echo Starting application...
schtasks /run /tn "%TASK_NAME%"

if %errorlevel% neq 0 (
    echo ERROR: Failed to start task!
    pause
    exit /b
)

pause
endlocal