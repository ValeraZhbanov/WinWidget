@echo off
setlocal EnableDelayedExpansion
chcp 65001 > nul

:: Admin rights check
if "%1"=="admin" (
    echo Started with admin rights
) else (
    echo Requesting admin rights...
    powershell -Command "Start-Process 'cmd.exe' -ArgumentList '/c \"\"%~f0\" admin\"' -Verb RunAs"
    exit /b
)

set "SCRIPT_PATH=%~dp0..\service.pyw"
set "TASK_NAME=WinWidgetTask"
set "PROCESS_NAME=python"
set "APP_TITLE=WinWidget"


wmic process where "name like '%%%PROCESS_NAME%%%' and commandline like '%%%APP_TITLE%%%'" call terminate

schtasks /delete /tn "%TASK_NAME%" /f

pause
endlocal