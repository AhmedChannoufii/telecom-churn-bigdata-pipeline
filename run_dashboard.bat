@echo off
cd /d "%~dp0"

echo ====================================================================
echo    LANCEMENT DU DASHBOARD DE RETENTION CLIENT (STREAMLIT)
echo ====================================================================
echo.

set PYTHON_EXE=C:\Users\chann\AppData\Local\Programs\Python\Python312\python.exe

start http://localhost:8501

"%PYTHON_EXE%" -m streamlit run src\dashboard.py --server.port 8501 --server.headless false

pause
