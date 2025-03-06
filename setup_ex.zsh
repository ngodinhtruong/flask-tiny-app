#!/bin/zsh

# Script to set up and run the Flask EX1 project using Zsh

# Enable colors for better output
autoload -U colors && colors

# Project directory path
PROJECT_DIR="."

# Main Flask file name
FLASK_FILE="tinny_app.py"

# Function to display error and exit
error_exit() {
    print -P "%F{red}[ERROR]%f $1"
    print "Press Enter to exit..."
    read -r
    exit 1
}

# Check for Python
print -P "%F{blue}Checking for Python...%f"
if ! command -v python3 &>/dev/null; then
    error_exit "Python is not installed. Please install Python before running this script.\nDownload Python from: https://www.python.org/downloads/"
fi

# Check for pip
print -P "%F{blue}Checking for pip...%f"
if ! command -v pip3 &>/dev/null; then
    error_exit "pip is not installed. Please install pip before proceeding.\nTry running: python3 -m ensurepip --upgrade\nThen: python3 -m pip install --upgrade pip"
fi

# Navigate to project directory
print -P "%F{blue}Navigating to project directory: $PROJECT_DIR...%f"
cd "$PROJECT_DIR" || error_exit "Could not navigate to $PROJECT_DIR. Check if the directory exists."

# Create virtual environment if it doesn't exist
if [[ ! -d "venv" ]]; then
    print -P "%F{blue}Creating virtual environment...%f"
    python3 -m venv venv || error_exit "Could not create virtual environment. Check permissions or Python installation."
fi

# Activate virtual environment
print -P "%F{blue}Activating virtual environment...%f"
# Use Unix-style path for Zsh (works on macOS/Linux, or WSL on Windows)
source venv/bin/activate || error_exit "Could not activate virtual environment. Check venv/bin/activate."

# Install dependencies from requirements.txt
if [[ -f "requirements.txt" ]]; then
    print -P "%F{blue}Installing dependencies from requirements.txt...%f"
    pip install -r requirements.txt || error_exit "Could not install dependencies from requirements.txt. Check the file or network connection."
else
    print -P "%F{yellow}[WARNING]%f requirements.txt not found. Installing Flask, Flask-SQLAlchemy, and Flask-Login manually..."
    pip install flask flask-sqlalchemy flask-login || error_exit "Could not install dependencies manually. Check network connection or pip."
fi

# Check for main Flask file
if [[ ! -f "$FLASK_FILE" ]]; then
    error_exit "Missing file $FLASK_FILE. The Flask project requires this file to run.\nEnsure $FLASK_FILE exists in $PROJECT_DIR."
fi

# Check for templates directory
if [[ ! -d "templates" ]]; then
    print -P "%F{yellow}[WARNING]%f 'templates' directory not found. HTML files should be in this directory."
    print "The application may fail if HTML files are missing."
fi

# Check for static directory
if [[ ! -d "static" ]]; then
    print -P "%F{yellow}[WARNING]%f 'static' directory not found. CSS and images should be in this directory."
    print "The application may fail if CSS or image files are missing."
fi

# Check for database directory and file
if [[ ! -d "database" ]]; then
    print -P "%F{yellow}[WARNING]%f 'database' directory not found. Flask-SQLAlchemy will create it on first run."
elif [[ ! -f "database/mydatabase.db" ]]; then
    print -P "%F{yellow}[WARNING]%f Database file mydatabase.db not found."
    print "Flask-SQLAlchemy will create it on first run."
fi

# Run the application
print -P "%F{blue}Starting Flask application...%f"
python3 "$FLASK_FILE" || error_exit "Could not run the application. Check the code in $FLASK_FILE or template/CSS files."

print -P "%F{green}Application is running at http://127.0.0.1:5000 (or another port if configured).%f"
# No 'pause' equivalent in Zsh by default, but we can wait for input if needed
print "Press Enter to continue..."
read -r