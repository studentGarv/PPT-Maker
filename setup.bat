@echo off
echo Setting up PPT Maker...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    exit /b 1
)

echo Python found!

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo To activate the virtual environment manually, run:
echo   venv\Scripts\activate.bat
echo.
echo To test the installation, run:
echo   python ppt_maker.py --test-connection
echo.
echo Make sure Ollama is installed and running:
echo   1. Install Ollama from https://ollama.ai
echo   2. Run: ollama serve
echo   3. Pull a model: ollama pull llama2
echo.
pause
