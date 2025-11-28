@echo off
REM JARVIS Launcher - Inicia JARVIS como programa

setlocal enabledelayedexpansion

REM Usar ruta absoluta del proyecto
set PROJECT_PATH=C:\Users\anune\PYTHON
cd /d "%PROJECT_PATH%"

REM Verificar que estamos en la carpeta correcta
if not exist "%PROJECT_PATH%\assistant\llm.py" (
    echo.
    echo Error: No se encontro el proyecto JARVIS en %PROJECT_PATH%
    echo.
    echo Verifica que la carpeta existe y contiene los archivos necesarios
    pause
    exit /b 1
)

REM Ejecutar JARVIS en modo híbrido (por defecto)
echo.
echo ========================================
echo  JARVIS Advanced v2.0 - Iniciando...
echo ========================================
echo.
echo Palabras clave: "JARVIS" u "Oye JARVIS"
echo Modo: Hibrido (voz + comando)
echo.
echo Di "JARVIS" o "Oye JARVIS" para activar escucha...
echo.

REM Activar venv y ejecutar
call .venv311\Scripts\activate.bat
python run_jarvis_voice.py --mode hybrid

REM Si llega aquí, JARVIS se cerró
pause
