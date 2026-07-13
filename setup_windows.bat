@echo off
setlocal
cd /d "%~dp0"

echo ================================================
echo Generative AI Search Optimizer - Windows Setup
echo ================================================

where py >nul 2>nul
if %errorlevel%==0 (
  set PYTHON=py
) else (
  where python >nul 2>nul
  if %errorlevel% neq 0 (
    echo Python was not found. Install Python 3.10 or newer from python.org.
    pause
    exit /b 1
  )
  set PYTHON=python
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  %PYTHON% -m venv .venv
  if %errorlevel% neq 0 goto :error
)

echo Installing project dependencies...
call .venv\Scripts\python.exe -m pip install --upgrade pip
if %errorlevel% neq 0 goto :error
call .venv\Scripts\python.exe -m pip install -e ".[dev]"
if %errorlevel% neq 0 goto :error

echo.
echo Setup completed successfully.
echo Run run_dashboard.bat to open the product UI.
echo Run run_api.bat to start the REST API.
pause
exit /b 0

:error
echo.
echo Setup failed. Review the error messages above.
pause
exit /b 1
