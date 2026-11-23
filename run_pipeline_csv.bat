@echo off
cd /d "%~dp0"

echo ====================================================================
echo    PIPELINE CLASSIQUE : STOCKAGE FORMAT CSV (NON OPTIMISE)
echo ====================================================================
echo.

set PYTHON_EXE=C:\Users\chann\AppData\Local\Programs\Python\Python312\python.exe

"%PYTHON_EXE%" src\pipeline_csv.py

echo.
pause
