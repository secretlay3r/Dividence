@echo off
setlocal enabledelayedexpansion

:: Define the base title
set BASE_TITLE=Build Script by Valthrunner

:: Set up ESC for ANSI colors
call :setESC

:: Initial Title of the script
title %BASE_TITLE%

:: Check if Python is installed
title %BASE_TITLE% - Checking for Python Installation
echo Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo %ESC%[31mPython is not installed. Please install Python from https://www.python.org/%ESC%[0m
    pause
    exit /b
) else (
    echo %ESC%[32mPython is installed.%ESC%[0m
)

:: Check if Python is added to PATH
title %BASE_TITLE% - Checking if Python is in PATH
echo Checking if Python is added to PATH...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo %ESC%[31mPython is not in PATH. Please reinstall Python and check "Add Python to PATH" during installation.%ESC%[0m
    pause
    exit /b
) else (
    echo %ESC%[32mPython is in PATH.%ESC%[0m
)

:: Check if pip is installed
title %BASE_TITLE% - Checking for pip Installation
echo Checking for pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %ESC%[33mpip is not installed. Installing pip...%ESC%[0m
    python -m ensurepip --upgrade
    echo %ESC%[32mpip has been successfully installed.%ESC%[0m
) else (
    echo %ESC%[32mpip is installed.%ESC%[0m
)

:: Install necessary packages
title %BASE_TITLE% - Installing Dependencies
echo Installing dependencies...
pip install dearpygui mss numpy pywin32 pyautogui keyboard opencv-python pynput pyinstaller pyarmor

if %errorlevel% neq 0 (
    echo %ESC%[31mDependency installation failed. Please check your internet connection and try again.%ESC%[0m
    pause
    exit /b
) else (
    echo %ESC%[32mAll dependencies installed successfully.%ESC%[0m
)

:: Check if main.py exists in the current directory
title %BASE_TITLE% - Checking if main.py Exists
if not exist main.py (
    echo %ESC%[31mmain.py not found in the current directory.%ESC%[0m
    pause
    exit /b
)

:: Obfuscate and build the executable with Pyarmor and PyInstaller
title %BASE_TITLE% - Obfuscating and Building the Executable
echo %ESC%[33mObfuscating and building the executable... Please be patient.%ESC%[0m
pyarmor gen --pack onefile main.py

if %errorlevel% neq 0 (
    echo %ESC%[31mObfuscation and compilation failed.%ESC%[0m
    pause
    exit /b
)

:: Generate a semi-random string for renaming
title %BASE_TITLE% - Generating Random String for Executable Name
for /l %%a in (1,1,6) do set "randStr=!randStr!!random:~0,1!"

:: Rename the resulting main.exe
title %BASE_TITLE% - Renaming Executable
echo Renaming executable...
set "exeName=main%randStr%.exe"
ren dist\main.exe %exeName%

if exist dist\%exeName% (
    echo %ESC%[32mExecutable renamed to %exeName%.%ESC%[0m
) else (
    echo %ESC%[31mFailed to rename executable.%ESC%[0m
    pause
    exit /b
)

:: Open the folder containing the executable
title %BASE_TITLE% - Opening Folder with Executable
echo Opening the folder containing the executable...
explorer dist

:: Final step - build completed
title %BASE_TITLE% - Build Completed
echo %ESC%[32mBuild process completed successfully.%ESC%[0m
pause
exit /b

:: Function to set the ESC character for ANSI colors
:setESC
for /f "delims=#" %%a in ('"prompt #$E# & for %%b in (1) do rem"') do set "ESC=%%a"
exit /b