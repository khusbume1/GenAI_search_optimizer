@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo The project is not set up yet.
  echo Running setup_windows.bat first...
  call setup_windows.bat
  if %errorlevel% neq 0 exit /b 1
)

echo Starting Generative AI Search Optimizer dashboard...
echo The browser should open at http://localhost:8501
call .venv\Scripts\python.exe -m streamlit run dashboard.py
