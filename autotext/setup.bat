@echo off
echo ========================================
echo Station Monitoring System - Setup
echo ========================================
echo.

cd /d "%~dp0"

echo Creating virtual environment...
python -m venv station_monitor\venv

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to create virtual environment
    echo Make sure Python is installed
    pause
    exit /b 1
)

echo.
echo Installing Python dependencies...
call station_monitor\venv\Scripts\activate.bat
pip install -r station_monitor\requirements.txt
pip install packaging

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To start the application, run: run.bat
echo.
pause
