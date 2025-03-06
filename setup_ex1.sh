#!/bin/bash

# Script to set up and run the Flask EX1 project on Unix-like systems

# Project directory path
PROJECT_DIR="."

# Main Flask file name
FLASK_FILE="tinny_app.py"

# Function to display error and exit
error_exit() {
    echo "[ERROR] $1"
    echo "Press Enter to exit..."
    read
    exit 1
}

# Check for Python
echo "Checking for Python..."
if ! python3 --version >/dev/null 2>&1; then
    error_exit "Python is not installed. Please install Python before running this script.\nDownload Python from: https://www.python.org/downloads/"
fi

# Check for pip
echo "Checking for pip..."
if ! pip3 --version >/dev/null 2>&1; then
    error_exit "pip is not installed. Please install pip before proceeding.\nTry running: python3 -m ensurepip --upgrade\nThen: python3 -m pip install --upgrade pip"
fi

# Navigate to project directory
echo "Navigating to project directory: $PROJECT_DIR..."
cd "$PROJECT_DIR" || error_exit "Could not navigate to $PROJECT_DIR. Check if the directory exists."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv || error_exit "Could not create virtual environment. Check permissions or Python installation."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || error_exit "Could not activate virtual environment. Check venv/bin/activate."

# Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt || error_exit "Could not install dependencies from requirements.txt. Check the file or network connection."
else
    echo "[WARNING] requirements.txt not found. Installing Flask, Flask-SQLAlchemy, and Flask-Login manually..."
    pip install flask flask-sqlalchemy flask-login || error_exit "Could not install dependencies manually. Check network connection or pip."
fi

# Check for main Flask file
if [ ! -f "$FLASK_FILE" ]; then
    error_exit "Missing file $FLASK_FILE. The Flask project requires this file to run.\nEnsure $FLASK_FILE exists in $PROJECT_DIR."
fi

# Check for templates directory
if [ ! -d "templates" ]; then
    echo "[WARNING] 'templates' directory not found. HTML files should be in this directory."
    echo "The application may fail if HTML files are missing."
fi

# Check for static directory
if [ ! -d "static" ]; then
    echo "[WARNING] 'static' directory not found. CSS and images should be in this directory."
    echo "The application may fail if CSS or image files are missing."
fi

# Check for database directory and file
if [ ! -d "database" ]; then
    echo "[WARNING] 'database' directory not found. Flask-SQLAlchemy will create it on first run."
elif [ ! -f "database/mydatabase.db" ]; then
    echo "[WARNING] Database file mydatabase.db not found."
    echo "Flask-SQLAlchemy will create it on first run."
fi

# Run the application
echo "Starting Flask application..."
python3 "$FLASK_FILE" || error_exit "Could not run the application. Check the code in $FLASK_FILE or template/CSS files."

echo "Application is running at http://127.0.0.1:5000 (or another port if configured)."