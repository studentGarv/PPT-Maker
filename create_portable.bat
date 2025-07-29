@echo off
echo Creating portable PPT Maker package...

REM Create portable directory structure
if not exist "PPT-Maker-Portable" mkdir "PPT-Maker-Portable"
if not exist "PPT-Maker-Portable\python" mkdir "PPT-Maker-Portable\python"
if not exist "PPT-Maker-Portable\ollama" mkdir "PPT-Maker-Portable\ollama"
if not exist "PPT-Maker-Portable\app" mkdir "PPT-Maker-Portable\app"

echo Copying application files...
copy "*.py" "PPT-Maker-Portable\app\"
copy "requirements.txt" "PPT-Maker-Portable\app\"

echo Creating launcher script...
(
echo @echo off
echo echo Starting PPT Maker...
echo.
echo REM Set up portable Python path
echo set PYTHON_PATH=%%~dp0python
echo set PATH=%%PYTHON_PATH%%;%%PYTHON_PATH%%\Scripts;%%PATH%%
echo.
echo REM Start Ollama if not running
echo tasklist /FI "IMAGENAME eq ollama.exe" 2^>NUL ^| find /I /N "ollama.exe"^>NUL
echo if errorlevel 1 ^(
echo     echo Starting Ollama...
echo     start /B "%%~dp0ollama\ollama.exe" serve
echo     timeout /t 5 /nobreak ^> nul
echo ^)
echo.
echo REM Run PPT Maker
echo cd /d "%%~dp0app"
echo python ppt_maker.py %%*
echo.
echo pause
) > "PPT-Maker-Portable\PPT-Maker.bat"

echo Creating installation guide...
(
echo # PPT Maker Portable Installation Guide
echo.
echo ## What's Included
echo - Portable Python environment
echo - PPT Maker application
echo - Ollama AI engine
echo.
echo ## Setup Instructions
echo.
echo ### 1. Download Required Components
echo.
echo #### Python Portable:
echo 1. Download Python 3.11 Windows embeddable package from:
echo    https://www.python.org/downloads/windows/
echo 2. Extract to: PPT-Maker-Portable\python\
echo.
echo #### Ollama Portable:
echo 1. Download Ollama for Windows from:
echo    https://ollama.ai/download
echo 2. Extract/copy ollama.exe to: PPT-Maker-Portable\ollama\
echo.
echo ### 2. Install Python Dependencies
echo ```
echo cd PPT-Maker-Portable\app
echo ..\python\python.exe -m pip install -r requirements.txt
echo ```
echo.
echo ### 3. Download AI Model
echo ```
echo cd PPT-Maker-Portable
echo ollama\ollama.exe pull llama3
echo ```
echo.
echo ### 4. Usage
echo Double-click `PPT-Maker.bat` or run:
echo ```
echo PPT-Maker.bat "Create a presentation about AI"
echo ```
echo.
echo ## Directory Structure
echo ```
echo PPT-Maker-Portable/
echo ├── PPT-Maker.bat          # Main launcher
echo ├── README.md              # This guide
echo ├── python/                # Portable Python
echo ├── ollama/                # Ollama executable
echo └── app/                   # PPT Maker application
echo ```
) > "PPT-Maker-Portable\README.md"

echo.
echo Portable package created in: PPT-Maker-Portable\
echo.
echo Next steps:
echo 1. Follow the README.md in the portable folder
echo 2. Download Python and Ollama components
echo 3. Install dependencies
echo 4. Use PPT-Maker.bat to run
echo.
pause
