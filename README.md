![](https://api.visitorbadge.io/api/VisitorHit?user=secretlay3r&repo=Dividence-for-Spectre-Divide&countColor=%237B1E7A)
[![GitHub stars](https://img.shields.io/github/stars/secretlay3r/Dividence-for-Spectre-Divide)](https://github.com/secretlay3r/Dividence-for-Spectre-Divide/stargazers)

# Dividence-for-Spectre-Divide

**Visual cheat done for research purposes.**

This project includes features such as no-recoil, aimbot and triggerbot built using Python and DearPyGui.

## Features

- Color-based Aimbot
- Color-based Triggerbot
- No-Recoil

## How to install
**Navigate to [releases](https://github.com/secretlay3r/Dividence-for-Spectre-Divide/releases/tag/exe) and download latest version (it's not obfuscated!)**

## How to compile
1. **Download the repository**  

   Download the repository to your PC.

3. **Install Python**
   
   Make sure Python is installed. You can download it from [python.org](https://www.python.org/downloads/).  
   During installation, check the box to "Add Python to PATH".

5. **Install Dependencies**
   
   Open a command prompt and run the following command to install the required dependencies:

   ```bash
   pip install dearpygui mss numpy pywin32 pyautogui
6. **Compiling**

   I highly recommend obfuscating the .exe as it can be detected, but here are the basic compilation instructions.
   Open a command prompt IN DIRECTORY WITH ALL SCRIPTS and run the following command to compile all files to exe:
   
   ```bash
   pyinstaller --onefile --name Dividence main.py norecoil.py aimbot.py triggerbot.py

