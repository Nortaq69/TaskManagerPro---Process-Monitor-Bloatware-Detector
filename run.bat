@echo off
title TaskManagerPro - Quick Start
color 0B

echo.
echo ========================================
echo    TaskManagerPro - Process Monitor
echo    Quick Start
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please run install_and_run.bat first
    echo.
    pause
    exit /b 1
)

echo Starting TaskManagerPro...
echo.

:: Run the launcher
python launcher.py

echo.
echo TaskManagerPro has been closed.
echo.
pause
