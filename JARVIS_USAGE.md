# JARVIS Assistant - Guía de Uso (Backend Remoto)

## Estado Actual

El asistente JARVIS está configurado con un **backend remoto** (Hugging Face Inference API) ya que el binding local (`llama-cpp-python`) no fue compilado exitosamente en tu entorno Windows.

## ¿Cómo funciona?

1. **LocalLLM** intenta cargar el modelo local (`llama_cpp`). Si no está disponible, automáticamente carga **RemoteLLM**.
2. **RemoteLLM** hace llamadas HTTP a la API de inferencia de Hugging Face usando un modelo que especifiques en `.env`.
3. El asistente responde en **español** y puede ejecutar comandos, abrir archivos, ajustar volumen y enviar correos.

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

- `mistralai/Mistral-7B-Instruct-v0.1` — Buena calidad, rápido
- `meta-llama/Llama-2-7b-chat` — Requiere token de acceso
- `HuggingFaceH4/zephyr-7b-beta` — Abierto, buena performance
- `microsoft/phi-2` — Ligero, eficiente

**Nota:** Si el modelo es "gated" (privado), necesitarás aceptar los términos en Hugging Face y usar un token válido.

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
Tú> Hola, ¿cómo estás?
JARVIS> Hola — soy tu asistente JARVIS local. Dime cómo te puedo ayudar.

Tú> !exec whoami
JARVIS> (ejecuta el comando y devuelve output)

Tú> !open C:\Windows\Notepad.exe
JARVIS> Abierto

Tú> !vol set 50
JARVIS> Volumen fijado a 50

Tú> !sendmail
JARVIS> (te pide: Para, Asunto, Cuerpo — usa SMTP_* en .env)

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

### Error: "[RemoteLLM error] 401 Client Error: Unauthorized"
**Solución:** Verifica tu `HF_API_KEY` en `.env` sea correcto.

### Error: "No module named 'llama_cpp'"
**Esperado:** No hay binding local. Usa el backend remoto configurando `REMOTE_PROVIDER` en `.env`.

### Error: "falta HF_API_KEY o REMOTE_MODEL en el entorno"
**Solución:** Asegúrate de que `.env` esté en `C:\Users\anune\PYTHON` y tenga:
```dotenv
REMOTE_PROVIDER=hf
HF_API_KEY=hf_...
REMOTE_MODEL=mistralai/Mistral-7B-Instruct-v0.1
```

## Alternativas Futuras

Si quieres volver a intentar el binding local:

1. Instala **Visual Studio Build Tools 2022** con soporte C/C++
2. Instala **CMake** en tu PATH
3. Reintenta: `.\.venv311\Scripts\python.exe -m pip install llama-cpp-python`

Luego el asistente detectará automáticamente y usará `llama_cpp` si el modelo está en `MODEL_PATH`.

---

**Fecha:** 27 de noviembre de 2025  
**Repositorio:** https://github.com/Alxjq-afk/my-ml  
**Branch:** main
