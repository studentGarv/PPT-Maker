# Build script for creating standalone executable
# Run this to create a distributable version

# Install PyInstaller
pip install pyinstaller

# Create standalone executable
pyinstaller --onefile --name "PPT-Maker" --icon=icon.ico ppt_maker.py

# The executable will be in the 'dist' folder
# Users can run: PPT-Maker.exe "Create a presentation about AI"
