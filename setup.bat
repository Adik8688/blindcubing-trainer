@echo off
cd /d "%~dp0"  REM Change to the script's directory

call venv\Scripts\activate

cd Code

python main.py
