@echo off
title AI Healthcare Chatbot Server
echo ========================================
echo    AI HEALTHCARE CHATBOT SERVER
echo ========================================
echo.
echo Starting the healthcare chatbot...
echo Open your browser and go to: http://localhost:5000
echo.

cd /d "%~dp0"

"C:/Users/balaj/AppData/Local/Programs/Python/Python313/python.exe" app.py

echo.
echo Server has stopped.
pause