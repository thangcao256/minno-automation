@echo off
echo ======================================================
echo   DANG KHOI CHAY BO TEST SUITE (LOCAL)
echo ======================================================

:: 1. Kiem tra thu muc .venv
if not exist ".venv" (
    echo [ERROR] Khong tim thay moi truong ao .venv.
    echo Vui long chay setup.bat truoc!
    pause
    exit /b
)

:: 2. Kick hoat moi truong ao
call .venv\Scripts\activate

:: 3. Chay Pytest voi danh sach tu test_suite.txt
echo [RUNNING] Dang doc test_suite.txt va chay kiem thu...
echo.

:: Su dung PowerShell de loc file vi batch script xu ly grep hoi kem
powershell -Command "pytest (Get-Content test_suite.txt | Where-Object { $_ -notmatch '^#' -and $_ -ne '' }) --headed"

echo.
echo ======================================================
echo   KIEM THU HOAN TAT!
echo ======================================================
pause
