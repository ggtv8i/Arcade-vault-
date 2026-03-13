@echo off
title Arcade Vault — HTTP Server
echo ==========================================
echo   Arcade Vault - Simple HTTP Server
echo ==========================================
echo.
echo   افتح في المتصفح:
echo   http://localhost:8080/index.html
echo.
echo   Ctrl+C للإيقاف
echo ==========================================
echo.
python -m http.server 8080 2>nul || py -m http.server 8080 2>nul || (
  echo ERROR: Python غير مثبت
  echo ثبّته من: https://python.org
  pause
)
