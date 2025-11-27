@echo off
REM JARVIS Launcher - Inicia JARVIS como programa
REM Este archivo debería estar en el escritorio

setlocal enabledelayedexpansion

REM Obtener ruta de este script
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Ir a la carpeta del proyecto
cd ..\..

REM Verificar que estamos en la carpeta correcta
if not exist "assistant\llm.py" (
    echo.
    echo Error: No se encontro la carpeta de JARVIS
    echo Este acceso directo debe estar en el escritorio
    echo y el proyecto en C:\Users\anune\PYTHON
    pause
    exit /b 1
)

REM Ejecutar JARVIS en modo híbrido (por defecto)
echo.
echo ========================================
echo  JARVIS Advanced v2.0 - Iniciando...
echo ========================================
echo.

REM Activar venv y ejecutar
call .venv311\Scripts\activate.bat
python run_jarvis_voice.py --mode hybrid

REM Si llega aquí, JARVIS se cerró
pause
