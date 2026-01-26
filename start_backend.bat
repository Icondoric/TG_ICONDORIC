@echo off
cd backend
echo Starting Backend...
uvicorn app.main:app --reload
pause
