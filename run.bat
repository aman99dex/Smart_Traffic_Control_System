@echo off
REM Smart Traffic Control System - Quick Start Script (Windows)
REM This script sets up and runs the Smart Traffic Control System

echo ==========================================
echo Smart Traffic Control System - Setup
echo ==========================================

REM Check Python version
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo Found Python %python_version%

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

REM Run tests
echo Running system tests...
python test_system.py

if errorlevel 1 (
    echo Error: Tests failed. Please check the output above.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Setup Complete! Starting application...
echo ==========================================

python Main.py
pause
