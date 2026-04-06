@echo off
cd /d "%~dp0"
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller
echo.
echo Building executable...
pyinstaller Screenshoter.spec
echo.
echo Done! Executable: dist\Screenshoter.exe
pause