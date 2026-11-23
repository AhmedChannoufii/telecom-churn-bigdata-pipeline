@echo off
cd /d "%~dp0"

echo ====================================================================
echo    EXECUTION DU PIPELINE BIG DATA : CHURN TELECOM
echo ====================================================================
echo.

set PYTHON_EXE=C:\Users\chann\AppData\Local\Programs\Python\Python312\python.exe

"%PYTHON_EXE%" src\pipeline.py

echo.
echo ====================================================================
echo    TRAITEMENT TERMINE ! Les resultats sont enregistres en Parquet.
echo ====================================================================
pause
