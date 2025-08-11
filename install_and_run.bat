@echo off
title TaskManagerPro - Install and Run
color 0A

echo.
echo ========================================
echo    TaskManagerPro - Process Monitor
echo    Install and Run Script
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    echo.
    pause
    exit /b 1
)

echo Python found. Checking version...
python --version
echo.

:: Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please ensure pip is installed with Python
    echo.
    pause
    exit /b 1
)

echo Installing dependencies...
echo.

:: Install requirements
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    echo.
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

:: Check if running as administrator
net session >nul 2>&1
if errorlevel 1 (
    echo WARNING: Not running as Administrator
    echo Some features may not work properly
    echo Consider running this script as Administrator
    echo.
)

echo Starting TaskManagerPro...
echo.

:: Run the launcher
python launcher.py

echo.
echo TaskManagerPro has been closed.
echo.
pause
