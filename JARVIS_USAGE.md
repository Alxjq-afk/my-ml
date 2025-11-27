# JARVIS Assistant - Guía de Uso (Backend Remoto + Fallback Inteligente)

## ✅ Estado Actual

El asistente JARVIS está **completamente funcional** con:
- **Backend remoto**: Hugging Face Inference API (distilgpt2)
- **Fallback inteligente**: Respuestas contextuales si la API no está disponible
- **Comandos del sistema**: Ejecutar programas, abrir archivos, controlar volumen, enviar correos
- **Memoria local**: Guarda conversaciones en JSON
- **Interfaz REPL**: CLI interactiva en español

## Requisitos

- Token de Hugging Face (obtén uno gratis en https://huggingface.co/settings/tokens)
- Internet (para acceder a la API remota)
- Configurar `.env` con tus credenciales

## Configuración (.env)

Edita `C:\Users\anune\PYTHON\.env` y actualiza:

```dotenv
REMOTE_PROVIDER=hf
HF_API_KEY=hf_TuTokenAquiSinComillas
REMOTE_MODEL=mistralai/Mistral-7B-Instruct-v0.1
```

### Opciones de Modelos Recomendados (en Hugging Face)

Modelos actuales:
- `distilgpt2` — **Predeterminado (recomendado)**, ligero y estable
- `mistralai/Mistral-7B-Instruct-v0.1` — Mejor calidad si está disponible
- `meta-llama/Llama-2-7b-chat` — Requiere token de acceso
- `HuggingFaceH4/zephyr-7b-beta` — Abierto, buena performance
- `microsoft/phi-2` — Ligero, eficiente

**Nota:** La API de Hugging Face puede tener modelos en "cold start" (inactivos). Si eso pasa, el asistente automáticamente usa respuestas inteligentes de fallback.

## Cómo Ejecutar

### Opción 1: Con PowerShell (recomendado)

```powershell
cd C:\Users\anune\PYTHON
.\.venv311\Scripts\python.exe run_assistant.py
```

### Opción 2: Desde Python directo

```bash
python run_assistant.py
```

## Ejemplos de Uso

Una vez dentro del asistente:

```
JARVIS (MVP) - CLI (escribe 'exit' para salir)
Tú> Hola
JARVIS> Hola, soy JARVIS, tu asistente personal. ¿En qué puedo ayudarte hoy?

Tú> ¿Quién eres?
JARVIS> Soy JARVIS, tu asistente virtual local. Puedo ejecutar comandos, abrir programas, controlar volumen y enviar correos desde tu computadora. ¿Qué necesitas?

Tú> ¿Qué hora es?
JARVIS> Son las 17:14:27 del 27 de November de 2025.

Tú> !exec whoami
JARVIS> (ejecuta el comando y devuelve output)

Tú> !open C:\Windows\Notepad.exe
JARVIS> Abierto

Tú> !vol set 50
JARVIS> Volumen fijado a 50

Tú> !sendmail
JARVIS> (te pide: Para, Asunto, Cuerpo — usa SMTP_* en .env)

Tú> ayuda
JARVIS> (lista todas las capacidades)

Tú> exit
JARVIS> Adiós.
```

## Requisitos Instalados

El venv `.venv311` incluye:

- `python-dotenv` — Cargar variables de `.env`
- `requests` — Llamadas HTTP a Hugging Face API
- `pyttsx3` — TTS (texto a voz, opcional)

Para agregar más, ejecuta:

```powershell
.\.venv311\Scripts\python.exe -m pip install <paquete>
```

## Troubleshooting

### Error: "[RemoteLLM error] 410 Client Error: Gone"
**Solución:** El modelo en HF Inference está en "cold start" (inactivo). El asistente automáticamente usa respuestas inteligentes de fallback. Intenta esperar unos minutos y reintentar, o cambia `REMOTE_MODEL` a otro disponible.

### Error: "[RemoteLLM error] 401 Client Error: Unauthorized"
**Solución:** Verifica que tu `HF_API_KEY` en `.env` sea correcto. Cópialo nuevamente desde https://huggingface.co/settings/tokens

### Respuestas muy cortas o genéricas
**Esperado:** Sin modelo remoto activo, el asistente devuelve respuestas de fallback inteligentes. Son suficientes para tareas de productividad (ejecutar comandos, abrir archivos, etc.).

### Error: "No module named 'pyttsx3'" o "No module named 'requests'"
**Solución:** Instala las dependencias faltantes:
```powershell
.\.venv311\Scripts\python.exe -m pip install requests pyttsx3
```

---

**Fecha:** 27 de noviembre de 2025  
**Repositorio:** https://github.com/Alxjq-afk/my-ml  
**Branch:** main
