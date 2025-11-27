# JARVIS Advanced v2.0

Asistente de voz tipo Cortana/Alexa con escucha continua, STT, LLM e integración de APIs.

## 🎯 Características

### Backend LLM
- **Mistral 7B** local (4.37 GB GGUF) - cuando llama-cpp-python compile en tu sistema
- **Hugging Face Inference API** - fallback remoto (configurado por defecto)
- Respuestas inteligentes contextuales si ambos fallan

### Speech-to-Text (STT)
- **OpenAI Whisper** con soporte español
- Modelos: tiny, base (default), small, medium
- Transcripción en tiempo real desde micrófono

### Wake Word Detection
- Detecta "Hey JARVIS" para activar escucha
- Google Speech Recognition como base (requiere internet)
- PocketSphinx como alternativa local (sin internet)

### Intérpretes & Comandos
- **CommandInterpreter**: Comandos naturales sin prefijo (ej: "abre notepad")
- Ejecución automática de: exec, open, volume, sendmail
- Detección de intenciones en español

### APIs Integradas
- ⏰ Hora, fecha, zona horaria
- 🌍 Búsqueda web (DuckDuckGo, sin API key)
- 📊 Info del sistema (CPU, memoria, disco)
- 🧮 Cálculos matemáticos seguros

### Text-to-Speech (TTS)
- pyttsx3 (local, sin calidad)
- Habla respuestas automáticamente

### Memoria
- Conversaciones guardadas en JSON local
- Historial persistente

## 📦 Instalación

### 1. Dependencias base
```bash
pip install -r requirements.txt
```

### 2. Dependencias de voz
Ya instaladas:
```bash
pip install openai-whisper pyaudio scipy librosa speech-recognition pocketsphinx
pip install sounddevice requests python-dotenv psutil
```

### 3. Mistral 7B (opcional, pero recomendado)
Archivo ya descargado en: `C:\Users\anune\models\mistral-7b-instruct-v0.1.Q4_K_M.gguf`

Para usar localmente, compilar **llama-cpp-python**:
```bash
# Requiere Visual Studio Build Tools en Windows
pip install llama-cpp-python
```

### 4. Token Hugging Face
Agregado en `.env`:
```
REMOTE_PROVIDER=hf
HF_API_KEY=<tu_token_aqui>  # Registrate en huggingface.co
REMOTE_MODEL=distilgpt2
```

> ⚠️ **Importante**: Nunca compartas tu token HF públicamente. Es una credencial sensible.

## 🎤 Modos de ejecución

### CLI Mode (Texto)
```bash
python run_jarvis_voice.py --mode cli
```
Escribe comandos como en `run_assistant.py`

### Voice Mode (Voz)
```bash
python run_jarvis_voice.py --mode voice
```
- Escucha continua
- Di "Hey JARVIS" para activar
- Responde por voz

### Hybrid Mode (Auto, default)
```bash
python run_jarvis_voice.py
```
- CLI por defecto
- Activación por voz detecta comandos

## ⚙️ Opciones

```bash
python run_jarvis_voice.py \
  --mode hybrid \                 # cli, voice, hybrid
  --confirm-actions \             # Pedir confirmación
  --no-tts \                      # Desabilitar síntesis de voz
  --stt-model small               # tiny, base, small, medium
```

## 📝 Comandos Naturales

Sin necesidad de prefijos:

```
"abre notepad"              → Abre Notepad
"ejecuta dir C:\"           → Ejecuta comando dir
"sube volumen a 70"         → Ajusta volumen a 70%
"baja volumen"              → Baja volumen 10%
"envía un correo"           → Inicia envío de email
"¿Qué hora es?"             → Pregunta a JARVIS
"¿Cuál es la capital...?"   → Conversación normal
```

## 🏗️ Arquitectura

```
assistant/
  ├── config.py         # Carga .env
  ├── llm.py            # LocalLLM (Mistral) + RemoteLLM (HF)
  ├── memory.py         # Historial JSON
  ├── executor.py       # Ejecuta comandos
  ├── voice.py          # TTS (pyttsx3)
  ├── interpreter.py    # CommandInterpreter (natural language)
  ├── stt.py            # WhisperSTT (Speech-to-Text)
  ├── wake_word.py      # WakeWordDetector ("Hey JARVIS")
  └── apis.py           # Hora, búsqueda, clima, etc.

run_jarvis_voice.py       # CLI principal con voz
test_apis.py              # Tests de APIs
test_mistral.py           # Tests de LLM
```

## 🔧 Troubleshooting

### "llama-cpp-python no disponible"
- Requiere compilación con Visual Studio Build Tools
- Por ahora, JARVIS usa Hugging Face como fallback
- Token HF ya configurado en `.env`

### No se escucha micrófono
```bash
# Verificar dispositivos de audio
python -c "import sounddevice as sd; print(sd.query_devices())"
```

### Whisper tarda mucho
- Usa `--stt-model tiny` para inferencia más rápida
- O descarga modelo más pequeño

### Google Speech Recognition falla
- Necesita conexión a internet
- Intenta con micrófono más cercano
- Verifica que no haya bloqueadores

## 📊 Benchmarks

- **Whisper (base)**: ~5-10 segundos por grabación (CPU)
- **Mistral 7B (local)**: ~2-5 tokens/seg (CPU-only, lento)
- **Hugging Face API**: ~0.5-1 segundo (remoto, rápido)
- **Total flujo (voz)**: ~15-20 segundos end-to-end

## 🚀 Mejoras futuras

- [ ] Compilar llama-cpp-python con CUDA para GPU
- [ ] Usar Ollama para Mistral local más rápido
- [ ] Integrar Cortana/Windows Speech Recognition nativa
- [ ] Agregar smart home integration (Philips Hue, etc.)
- [ ] Machine learning para detección de intenciones
- [ ] Integrar con calendarios y email
- [ ] Soporte para múltiples idiomas

## 📄 Licencia

Mismo proyecto que `my-ml` - Educational

---

**Versión**: 2.0 (Advanced Voice)  
**Fecha**: Noviembre 2025  
**Autor**: Tu nombre
