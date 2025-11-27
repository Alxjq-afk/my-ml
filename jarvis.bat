@echo off
REM Script de inicio rápido para JARVIS Advanced v2.0

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║          JARVIS Advanced v2.0 - Voice Assistant                 ║
echo ║        Asistente de voz tipo Cortana/Alexa                      ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Verificar que estamos en la carpeta correcta
if not exist "assistant\llm.py" (
    echo ❌ Error: Este script debe ejecutarse desde C:\Users\anune\PYTHON
    pause
    exit /b 1
)

echo Selecciona el modo de ejecución:
echo.
echo 1. CLI Mode (Texto solamente)
echo 2. Voice Mode (Escucha continua)
echo 3. Hybrid Mode (Auto-detecta)
echo 4. Demo Interactiva
echo 5. Demo Rápida
echo.

set /p choice="Selecciona opción (1-5): "

if "%choice%"=="1" (
    echo.
    echo 🖥️  Iniciando JARVIS en modo CLI...
    echo.
    python run_jarvis_voice.py --mode cli
) else if "%choice%"=="2" (
    echo.
    echo 🎤 Iniciando JARVIS en modo Voice...
    echo.
    python run_jarvis_voice.py --mode voice
) else if "%choice%"=="3" (
    echo.
    echo 🤖 Iniciando JARVIS en modo Hybrid...
    echo.
    python run_jarvis_voice.py --mode hybrid
) else if "%choice%"=="4" (
    echo.
    echo 🎮 Iniciando Demo Interactiva...
    echo.
    python demo_jarvis.py
) else if "%choice%"=="5" (
    echo.
    echo ⚡ Ejecutando Demo Rápida...
    echo.
    python demo_quick.py
    pause
) else (
    echo ❌ Opción no válida
    pause
    exit /b 1
)

pause
