@echo off
echo Activando entorno virtual...
call "%~dp0venv\Scripts\activate.bat"
echo Starting Backend...
cd "%~dp0backend"
uvicorn app.main:app --reload
pause
