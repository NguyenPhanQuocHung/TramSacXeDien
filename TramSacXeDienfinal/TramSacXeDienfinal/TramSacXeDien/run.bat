@echo off
REM Chuyển đến thư mục của script này
cd /d "%~dp0"

echo ==========================================
echo Toi Uu Hoa Vi Tri Tram Sac Xe Dien
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Install requirements
echo [INFO] Checking and installing requirements...
pip install -q -r requirements.txt

REM Start Flask app
echo.
echo [INFO] Starting Flask application...
echo [INFO] Open your browser and go to: http://127.0.0.1:5000
echo.r
python app.py
pause
