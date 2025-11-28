"""
Módulo de voz mejorado con soporte para pyttsx3 (fallback) y Coqui TTS (premium offline).

Estrategia de fallback:
1. Intentar Coqui TTS (mejor calidad, modelos offline)
2. Si no está disponible o falla, usar pyttsx3 (más ligero)
"""
import os

try:
    from TTS.api import TTS
    _HAS_COQUI = True
except Exception:
    _HAS_COQUI = False

try:
    import pyttsx3
    _HAS_PYTTSX3 = True
except Exception:
    _HAS_PYTTSX3 = False


_COQUI_ENGINE = None
_PYTTSX3_ENGINE = None


def get_available_engines():
    """Retorna dict con motores disponibles."""
    return {
        'coqui': _HAS_COQUI,
        'pyttsx3': _HAS_PYTTSX3,
    }


def init_coqui_tts(model_name="tts_models/es/mai/glow-tts", use_gpu=False):
    """
    Inicializar Coqui TTS con un modelo específico.
    
    Args:
        model_name: nombre del modelo (ej: "tts_models/es/mai/glow-tts")
        use_gpu: usar GPU si está disponible
    
    Returns:
        TTS engine o None si falla
    """
    global _COQUI_ENGINE
    if not _HAS_COQUI:
        return None
    
    try:
        if _COQUI_ENGINE is None:
            print(f"🎵 Cargando modelo Coqui TTS: {model_name}")
            _COQUI_ENGINE = TTS(model_name=model_name, gpu=use_gpu, verbose=False)
        return _COQUI_ENGINE
    except Exception as e:
        print(f"⚠ Error inicializando Coqui TTS: {e}")
        return None


def _init_pyttsx3():
    """Inicializar pyttsx3 una vez."""
    global _PYTTSX3_ENGINE
    if not _HAS_PYTTSX3:
        return None
    if _PYTTSX3_ENGINE is not None:
        return _PYTTSX3_ENGINE
    
    engine = pyttsx3.init()
    
    # Buscar voz en español
    voices = engine.getProperty('voices')
    selected = None
    for v in voices:
        name = getattr(v, 'name', '') or getattr(v, 'id', '')
        langs = getattr(v, 'languages', []) or []
        if any('es' in str(l).lower() for l in langs) or 'spanish' in name.lower() or 'es-' in name.lower():
            selected = v
            break
    
    if selected is None and voices:
        selected = voices[0]
    
    try:
        if selected is not None:
            engine.setProperty('voice', selected.id)
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.95)
    except Exception:
        pass
    
    _PYTTSX3_ENGINE = engine
    return _PYTTSX3_ENGINE


def speak(text: str, engine_preference="coqui", model_name="tts_models/es/mai/glow-tts", save_to_file=None):
    """
    Sintetizar y reproducir texto.
    
    Args:
        text: texto a sintetizar
        engine_preference: "coqui" (preferencia) o "pyttsx3" (fallback)
        model_name: modelo Coqui a usar (ej: "tts_models/es/mai/glow-tts")
        save_to_file: (opcional) guardar WAV en archivo en lugar de reproducir
    
    Returns:
        True si es exitoso, False si falla
    """
    # Intentar Coqui TTS si está disponible y se prefiere
    if engine_preference == "coqui" and _HAS_COQUI:
        try:
            tts = init_coqui_tts(model_name)
            if tts is not None:
                if save_to_file:
                    print(f"🔊 Sintetizando con Coqui TTS → {save_to_file}")
                    tts.tts_to_file(text=text, file_path=save_to_file)
                    return True
                else:
                    print(f"🔊 Sintetizando con Coqui TTS...")
                    tts.tts_to_file(text=text, file_path="/tmp/jarvis_tts.wav")
                    # Reproducir con sistema
                    try:
                        import subprocess
                        subprocess.run(["/tmp/jarvis_tts.wav"], check=True)
                    except Exception:
                        # Fallback: solo guardar silenciosamente
                        pass
                    return True
        except Exception as e:
            print(f"⚠ Coqui TTS falló: {e}. Usando fallback pyttsx3...")
    
    # Fallback a pyttsx3
    if _HAS_PYTTSX3:
        try:
            engine = _init_pyttsx3()
            if engine is None:
                return False
            if save_to_file:
                engine.save_to_file(text, save_to_file)
                engine.runAndWait()
            else:
                engine.say(text)
                engine.runAndWait()
            return True
        except Exception as e:
            print(f"❌ Error en TTS: {e}")
            return False
    
    # Si nada funciona
    print("[TTS no disponible]", text)
    return False


def list_coqui_models():
    """Listar modelos Coqui TTS disponibles (documentación)."""
    models = {
        "es/mai/glow-tts": "Español (MAI) - Glow-TTS - Recomendado para español",
        "es/css10/glow-tts": "Español (CSS10) - Glow-TTS",
        "en/ljspeech/glow-tts": "Inglés (LJSpeech) - Glow-TTS - Profesional",
        "en/ljspeech/tacotron2-DDC": "Inglés (LJSpeech) - Tacotron2",
        "en/glow-tts": "Inglés - Glow-TTS",
    }
    return models


if __name__ == "__main__":
    # Test rápido
    print("=== Test de Módulo de Voz ===\n")
    print(f"Motores disponibles: {get_available_engines()}")
    
    if _HAS_COQUI:
        print("\n✓ Coqui TTS disponible")
        print(f"Modelos recomendados: {list_coqui_models()}")
    else:
        print("\n⚠ Coqui TTS no instalado")
    
    if _HAS_PYTTSX3:
        print("✓ pyttsx3 disponible (fallback)")
    else:
        print("⚠ pyttsx3 no instalado")
    
    # Test de síntesis
    print("\nProbando síntesis...")
    result = speak("Hola, soy JARVIS. Test de síntesis de voz.", engine_preference="coqui")
    print(f"Resultado: {'Exitoso' if result else 'Falló'}")
