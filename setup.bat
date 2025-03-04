@echo off
cd /d "%~dp0" || echo Failed to change directory.

call venv\Scripts\activate.bat || echo Failed to activate venv.

python -m Code.main || echo Failed to run script.