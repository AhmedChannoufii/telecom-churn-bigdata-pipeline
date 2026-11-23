@echo off
cd /d "%~dp0"

echo ====================================================================
echo    PIPELINE BIG DATA : STOCKAGE FORMAT APACHE PARQUET (OPTIMISE)
echo ====================================================================
echo.

set PYTHON_EXE=C:\Users\chann\AppData\Local\Programs\Python\Python312\python.exe

"%PYTHON_EXE%" src\pipeline_parquet.py

echo.
pause
