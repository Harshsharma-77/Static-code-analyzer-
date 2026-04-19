@echo off
echo =========================================
echo Starting CodeScan Compiler...
echo =========================================
echo Installing/Checking Dependencies...
pip install -r requirements.txt

echo.
echo Starting Server...
python main.py
pause
