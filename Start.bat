@echo off
cd /d "%~dp0"

:: Проверка Python
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

:: Активация venv
call "venv\Scripts\activate.bat"

:: Установка зависимостей
if exist "requirements.txt" (
    pip install -r requirements.txt
)

:: Запуск программы
python ui.py
pause