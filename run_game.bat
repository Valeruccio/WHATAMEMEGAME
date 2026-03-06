@echo off
REM Запуск игры "Что за мем" из текущей папки
cd /d "%~dp0"
python mem_game_manager.py
pause

