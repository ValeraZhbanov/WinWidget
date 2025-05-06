@echo off
setlocal enabledelayedexpansion

set "SERVICE_NAME=WinWidgetService"

echo Checking status of %SERVICE_NAME% service...

sc query "%SERVICE_NAME%" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INSTALLED]
    sc query "%SERVICE_NAME%" | findstr /C:"RUNNING" >nul
    if %errorlevel% equ 0 (
        echo Status: RUNNING
    ) else (
        sc query "%SERVICE_NAME%" | findstr /C:"STOPPED" >nul
        if %errorlevel% equ 0 (
            echo Status: STOPPED
        ) else (
            echo Status: UNKNOWN
        )
    )
    
    :: Дополнительная информация
    echo.
    echo Service configuration:
    sc qc "%SERVICE_NAME%"
) else (
    echo [NOT INSTALLED]
)

pause