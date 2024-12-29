import os
import sys
import PyInstaller.__main__

def build_exe():
    # Create resource directories
    os.makedirs('images', exist_ok=True)
    os.makedirs('sounds', exist_ok=True)
    
    # PyInstaller options
    options = [
        'main.py',  # Your main script
        '--onefile',  # Create a single executable
        '--noconsole',  # Don't show console window
        '--icon=icon.ico',  # Use custom icon
        '--name=Plants vs Zombies',  # Name of the executable
        '--clean',  # Clean PyInstaller cache
        '--noconfirm',  # Replace output directory without asking
        '--add-data=sounds/*.wav;sounds',  # Include sound files
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(options)

if __name__ == '__main__':
    build_exe()
