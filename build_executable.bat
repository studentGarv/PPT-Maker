@echo off
echo Building standalone executable for PPT Maker...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is required to build the executable
    echo Please install Python 3.7+ from https://python.org
    exit /b 1
)

echo Installing PyInstaller...
pip install pyinstaller

echo Building executable...
pyinstaller --onefile ^
    --name "PPT-Maker" ^
    --add-data "config.py;." ^
    --hidden-import=ollama ^
    --hidden-import=pptx ^
    ppt_maker.py

echo.
echo Build complete!
echo.
echo The executable is located at: dist\PPT-Maker.exe
echo.
pause