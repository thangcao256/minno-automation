@echo off
echo ======================================================
echo   DANG THIET LAP MOI TRUONG KIEM THU MINNOSOFT
echo ======================================================

:: 1. Kiem tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python chua duoc cai dat. Vui long cai Python truoc!
    pause
    exit /b
)

:: 2. Tao moi truong ao (Virtual Environment)
echo [1/4] Dang tao moi truong ao (.venv)...
python -m venv .venv

:: 3. Kick hoat moi truong ao va cai thu vien
echo [2/4] Dang cai dat thu vien tu requirements.txt...
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

:: 4. Cai dat Playwright Browsers
echo [3/4] Dang tai trinh duyet Playwright (Chromium)...
playwright install chromium

:: 5. Hoan tat
echo [4/4] THIET LAP HOAN TAT!
echo.
echo Huong dan:
echo 1. Trong PyCharm, vao Settings -> Project -> Python Interpreter.
echo 2. Chon 'Add Interpreter' -> 'Existing' -> Tro den .venv\Scripts\python.exe.
echo 3. Bay gio ban co the nhan nut mui ten xanh de chay test!
echo.
pause
