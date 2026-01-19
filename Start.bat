@echo off
cd /d "%~dp0"


python --version >nul 2>&1
if errorlevel 1 (
    echo Python не найден!
    pause
    exit /b 1
)

:: Создание venv если нет
if not exist "venv\" (
    echo Создание виртуальной среды...
    python -m venv venv
)


call "venv\Scripts\activate.bat"


if exist "requirements.txt" (
    pip install -r requirements.txt
)


python ui.py

pause
