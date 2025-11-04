@echo off
cd /d "%~dp0station_monitor"
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)
python main.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Application failed to start.
    pause
    exit /b 1
)
