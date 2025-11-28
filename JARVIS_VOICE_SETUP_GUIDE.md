# JARVIS - Voz y Wake-Word Configurados

## Cambios Realizados (Hoy)

### 1. ✅ Wake-Words Simplificadas
- Ahora solo responde a: **"jarvis"** y **"oye jarvis"**
- Archivo: `assistant/wake_word.py`
- Soporta VOSK offline como detector principal
- Fallback a Google Speech Recognition si es necesario

### 2. ✅ Reconocimiento Offline (VOSK)
- **STT (Speech-to-Text):** VOSK modelo español (~40 MB en `assistant_data/models/vosk-model-small-es-0.22/`)
- **Wake-word:** VOSK detecta "jarvis" y "oye jarvis" completamente offline
- **Fallback:** Google Speech Recognition si VOSK falla

### 3. 🔄 Voz JARVIS (En Proceso)
Se está instalando **Coqui TTS** para una voz de mejor calidad offline.

**Estado:** La instalación de TTS (pip install TTS) está en progreso.
- Descargando dependencias: scipy, transformers, spacy, gruut_lang_es, etc.
- Tamaño total: ~500MB-1GB (con todos los idiomas)
- Primera descarga de modelos TTS: ~100MB por modelo

## Próximos Pasos (Una vez termine TTS)

### Paso 1: Esperar instalación de TTS
```powershell
# La instalación está en progreso. Espera a que termine (5-10 minutos aprox)
# Verifica el estado con:
C:\Users\anune\PYTHON\.venv311\Scripts\python.exe -m pip list | grep -i tts
```

### Paso 2: Ejecutar configuración de voz JARVIS
```powershell
C:\Users\anune\PYTHON\.venv311\Scripts\python.exe setup_jarvis_voice.py
```

Esto abrirá un menú para elegir:
1. **Español profesional (Recomendado)** - `tts_models/es/mai/glow-tts`
2. **Inglés profesional (JARVIS-like)** - `tts_models/en/ljspeech/glow-tts`
3. **Español alternativo** - `tts_models/es/css10/glow-tts`

Se descargará el modelo (~80-100 MB) y se creará una prueba de síntesis.

### Paso 3: Validar con launcher
```powershell
.\jarvis_launcher.bat
```

JARVIS ahora:
- ✅ Escucha solo "jarvis" / "oye jarvis" (offline)
- ✅ Responde con voz de alta calidad (Coqui TTS)
- ✅ Toda la conversación voz es offline (VOSK + Coqui TTS)
- ⚠️ LLM sigue siendo remoto (Hugging Face) — puedes instalar llama-cpp-python para local

## Archivos Creados/Modificados

| Archivo | Cambio | Descripción |
|---------|--------|-------------|
| `assistant/wake_word.py` | Modificado | Solo responde a ["jarvis", "oye jarvis"] |
| `assistant/voice_enhanced.py` | Nuevo | Soporte Coqui TTS + pyttsx3 fallback |
| `explore_voices.py` | Nuevo | Explora modelos TTS disponibles |
| `setup_jarvis_voice.py` | Nuevo | Asistente interactivo para elegir/instalar voz |
| `requirements.txt` | Modificado | Añadido `vosk`, comentado `TTS` (opcional) |

## Configuración Actual

**STT (Entrada de voz):**
- Motor: VOSK (offline, español)
- Fallback: Google Speech Recognition (online)
- Modelos: `assistant_data/models/vosk-model-small-es-0.22/`

**Wake-Word:**
- Palabras clave: "jarvis", "oye jarvis"
- Motor: VOSK (offline)
- Fallback: Google Speech Recognition

**TTS (Salida de voz):**
- Motor: Coqui TTS (en instalación) → mejor calidad
- Fallback: pyttsx3 (sistema operativo)
- Voces: Español profesional o Inglés (por elegir)

**LLM (Generación de respuestas):**
- Motor: Hugging Face remoto (requiere internet)
- Fallback: Training dataset local
- Opción: llama-cpp-python local (requiere instalación manual)

## Próxima Sesión

Una vez hayas ejecutado `setup_jarvis_voice.py` y confirmado que todo funciona:

1. ✅ Prueba el launcher: `.\jarvis_launcher.bat`
2. ✅ Di "jarvis" o "oye jarvis" para activar
3. ✅ Dicta un comando (ej: "qué hora es", "abre el navegador")
4. ✅ Escucha respuesta en voz JARVIS
5. 📝 Después: puedes hacer commit de cambios y explorar LLM local (llama-cpp-python)

---

**Nota:** Si en cualquier momento no quieres esperar a que termine TTS, puedes usar:
```powershell
.\jarvis_launcher.bat
```
Sin TTS instalado, JARVIS usará pyttsx3 (menos calidad pero funciona al instante).
