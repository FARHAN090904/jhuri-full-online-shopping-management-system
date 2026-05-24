@echo off
echo =============================================
echo   ShopBD Django Backend Setup
echo =============================================

:: Step 1: Create virtual environment
echo [1/5] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

:: Step 2: Install dependencies
echo [2/5] Installing dependencies...
pip install -r requirements.txt

:: Step 3: Check MySQL connection
echo [3/5] Make sure XAMPP MySQL is running on port 3306
echo       Database name: online_shopping
echo       User: root, Password: (empty)
pause

:: Step 4: Run server
echo [4/5] Starting Django server...
python manage.py runserver 0.0.0.0:8000

echo =============================================
echo   Server running at http://127.0.0.1:8000
echo =============================================
