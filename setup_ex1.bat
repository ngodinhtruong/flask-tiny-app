@echo off
REM Script to set up and run the Flask EX1 project on Windows

REM Project directory path
set PROJECT_DIR=.

REM Main Flask file name
set FLASK_FILE=tinny_app.py

REM Check for Python
echo Checking for Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed. Please install Python before running this script.
    echo Download Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check for pip
echo Checking for pip...
pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] pip is not installed. Please install pip before proceeding.
    echo Try running: python -m ensurepip --upgrade
    echo Then: python -m pip install --upgrade pip
    pause
    exit /b 1
)

REM Navigate to project directory
echo Navigating to project directory: %PROJECT_DIR%...
cd %PROJECT_DIR% || (
    echo [ERROR] Could not navigate to %PROJECT_DIR%. Check if the directory exists.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Could not create virtual environment. Check permissions or Python installation.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Could not activate virtual environment. Check venv\Scripts\activate.
    pause
    exit /b 1
)

REM Install dependencies from requirements.txt
if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Could not install dependencies from requirements.txt. Check the file or network connection.
        pause
        exit /b 1
    )
) else (
    echo [WARNING] requirements.txt not found. Installing Flask, Flask-SQLAlchemy, and Flask-Login manually...
    pip install flask flask-sqlalchemy flask-login
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Could not install dependencies manually. Check network connection or pip.
        pause
        exit /b 1
    )
)

REM Check for main Flask file
if not exist %FLASK_FILE% (
    echo [ERROR] Missing file %FLASK_FILE%. The Flask project requires this file to run.
    echo Ensure %FLASK_FILE% exists in %PROJECT_DIR%.
    pause
    exit /b 1
)

REM Check for templates directory
if not exist templates (
    echo [WARNING] 'templates' directory not found. HTML files should be in this directory.
    echo The application may fail if HTML files are missing.
)

REM Check for static directory
if not exist static (
    echo [WARNING] 'static' directory not found. CSS and images should be in this directory.
    echo The application may fail if CSS or image files are missing.
)

REM Check for database directory and file
if not exist database (
    echo [WARNING] 'database' directory not found. Flask-SQLAlchemy will create it on first run.
) else (
    if not exist database\mydatabase.db (
        echo [WARNING] Database file mydatabase.db not found.
        echo Flask-SQLAlchemy will create it on first run.
    )
)

REM Run the application
echo Starting Flask application...
python %FLASK_FILE%
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Could not run the application. Check the code in %FLASK_FILE% or template/CSS files.
    pause
    exit /b 1
)

echo Application is running at http://127.0.0.1:5000 (or another port if configured).
pause