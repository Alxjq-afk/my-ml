"""TTS y STT minimal: pyttsx3 para TTS y Vosk (opcional) para STT.

STT requiere descargar un modelo VOSK y configurar VOSK_MODEL_PATH en `.env`.
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


def speak(text: str):
    if not _HAS_TTS:
        print("[TTS no disponible]", text)
        return
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


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
