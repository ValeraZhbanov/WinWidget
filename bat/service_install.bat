@echo off
setlocal EnableDelayedExpansion
chcp 65001 > nul

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
set "PROCESS_NAME=python"
set "APP_TITLE=WinWidget"
set "PYTHONW_PATH="

where pythonw.exe >nul 2>&1
if %errorlevel% equ 0 (
    for /f "delims=" %%i in ('where pythonw.exe') do (
        set "PYTHONW_PATH=%%i"
        goto python_check
    )
)

for %%d in (
    "%LOCALAPPDATA%\Programs\Python\Python311\pythonw.exe",
    "%LOCALAPPDATA%\Programs\Python\Python310\pythonw.exe",
    "%APPDATA%\Python\Python311\pythonw.exe",
    "C:\Python311\pythonw.exe",
    "C:\Python310\pythonw.exe"
) do (
    if exist "%%~d" (
        set "PYTHONW_PATH=%%~d"
        goto python_check
    )
)

echo Python not found automatically.
set /p PYTHONW_PATH="Enter full path to pythonw.exe: "
if not exist "!PYTHONW_PATH!" (
    echo Invalid path provided
    pause
    exit /b 1
)

:python_check

echo %PYTHONW_PATH%

wmic process where "name like '%%%PROCESS_NAME%%%' and commandline like '%%%APP_TITLE%%%'" call terminate

schtasks /delete /tn "%TASK_NAME%" /f

pip install -U -r "%PYTHON_LIBS_PATH%"

schtasks /create /tn "%TASK_NAME%" /tr "\"%PYTHONW_PATH%\" \"%SCRIPT_PATH%\"" /sc onlogon /it /ru %USERNAME% /rl highest

schtasks /run /tn "%TASK_NAME%"

pause
endlocal