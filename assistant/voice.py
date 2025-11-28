"""TTS y STT: pyttsx3 para TTS (offline, SAPI5) y Vosk para STT.

Motor de síntesis:
- pyttsx3 (offline, basado en SAPI5 de Windows)
- Voces disponibles: todas las instaladas en el sistema operativo
- Para mejor calidad, se pueden instalar voces adicionales en Windows:
  Settings → Time & Language → Speech → Manage voices

Alternativa premium (requiere compilación C++):
- Coqui TTS (comentado en requirements.txt - requiere Visual C++ Build Tools)
"""
import os

try:
    import pyttsx3
    _HAS_TTS = True
except Exception:
    _HAS_TTS = False

try:
    from vosk import Model, KaldiRecognizer
    import sounddevice as sd
    _HAS_VOSK = True
except Exception:
    _HAS_VOSK = False


_ENGINE = None


def _init_engine(preferred_voice_name: str = "jarvis"):
    global _ENGINE
    if not _HAS_TTS:
        return None
    if _ENGINE is not None:
        return _ENGINE
    engine = pyttsx3.init()

    # Buscar voz preferida: primero por nombre que contenga 'jarvis'
    voices = engine.getProperty('voices')
    selected = None
    for v in voices:
        name = getattr(v, 'name', '') or getattr(v, 'id', '')
        if preferred_voice_name.lower() in name.lower():
            selected = v
            break

    # Si no encontramos 'jarvis', elegir primera voz claramente española
    if selected is None:
        for v in voices:
            # Algunos engines exponen idiomas en 'languages'
            langs = getattr(v, 'languages', []) or []
            name = getattr(v, 'name', '') or getattr(v, 'id', '')
            if any('es' in str(l).lower() or 'spanish' in str(l).lower() for l in langs) or 'spanish' in name.lower() or 'es-' in name.lower() or 'helena' in name.lower() or 'sabina' in name.lower() or 'javier' in name.lower():
                selected = v
                break

    # Fallback: primera voz disponible
    if selected is None and voices:
        selected = voices[0]

    try:
        if selected is not None:
            engine.setProperty('voice', selected.id)
        # Ajustes para timbre robótico/estilo JARVIS
        # Velocidad moderada (150 rate = voz clara y deliberada)
        # Volumen ligeramente reducido para menos artefactos
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.95)
        # Nota: SAPI5 en Windows no soporta pitch; el efecto JARVIS se logra con rate+volume
    except Exception:
        pass

    _ENGINE = engine
    return _ENGINE


def speak(text: str):
    if not _HAS_TTS:
        print("[TTS no disponible]", text)
        return
    engine = _init_engine()
    if engine is None:
        print("[TTS no disponible]", text)
        return
    engine.say(text)
    engine.runAndWait()


def list_voices():
    """Devuelve la lista de voces disponibles (name, id, languages)."""
    if not _HAS_TTS:
        return []
    engine = pyttsx3.init()
    voices = []
    for v in engine.getProperty('voices'):
        voices.append({'id': v.id, 'name': getattr(v, 'name', ''), 'languages': getattr(v, 'languages', [])})
    return voices


def listen(duration: int = 5) -> str:
    """Escucha audio del micrófono y devuelve texto si VOSK está disponible."""
    model_path = os.getenv("VOSK_MODEL_PATH")
    if not _HAS_VOSK or not model_path or not os.path.exists(model_path):
        return ""
    model = Model(model_path)
    rec = KaldiRecognizer(model, 16000)

    try:
        recording = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype="int16")
        sd.wait()
        data = recording.tobytes()
        if rec.AcceptWaveform(data):
            import json

            res = json.loads(rec.Result())
            return res.get("text", "")
        else:
            return ""
    except Exception:
        return ""
