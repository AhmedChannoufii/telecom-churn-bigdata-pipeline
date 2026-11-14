@echo off
echo ====================================================================
echo    LANCEMENT DU DASHBOARD DE RETENTION CLIENT (STREAMLIT)
echo ====================================================================
echo.

set PYTHON_EXE=C:\Users\chann\AppData\Local\Programs\Python\Python312\python.exe

"%PYTHON_EXE%" -m streamlit run src\dashboard.py

pause
