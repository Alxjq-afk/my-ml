#!/usr/bin/env python3
"""
Explorador de voces TTS - Buscar voz JARVIS.

Coqui TTS (basado en Glow-TTS, FastPitch, etc.) ofrece varias voces.
JARVIS es una IA británica, así que buscamos voces en inglés británico o español con tono profesional.
"""
import os
import sys

try:
    from TTS.api import TTS
except ImportError:
    print("TTS no está instalado. Instálalo con: pip install TTS")
    sys.exit(1)


def list_available_voices():
    """Listar modelos de TTS disponibles en Coqui."""
    print("=" * 70)
    print("Coqui TTS - Modelos y voces disponibles")
    print("=" * 70)
    
    # Modelos populares y sus voces
    models_info = {
        "tts_models/es/mai/glow-tts": "Español (Glow-TTS) - Recomendado para español",
        "tts_models/es/css10/glow-tts": "Español CSS10 (Glow-TTS)",
        "tts_models/en/ljspeech/glow-tts": "Inglés (LJSpeech Glow-TTS) - Voz profesional femenina",
        "tts_models/en/ljspeech/tacotron2-DDC": "Inglés (LJSpeech Tacotron2) - Voz natural femenina",
        "tts_models/en/glow-tts": "Inglés Glow-TTS - Recomendado para inglés",
        "tts_models/multilingual/multi-dataset/bark": "Multilingual Bark - Voces diversas (requiere ~10GB)",
    }
    
    print("\nModelos recomendados para JARVIS (IA británica/profesional):\n")
    for model, desc in models_info.items():
        print(f"  • {model}")
        print(f"    → {desc}\n")
    
    print("\nPara usar un modelo:")
    print("  model_name = 'tts_models/es/mai/glow-tts'  # Para español")
    print("  model_name = 'tts_models/en/ljspeech/glow-tts'  # Para inglés profesional")
    print("\nDetalles en: https://github.com/coqui-ai/TTS")


def test_voices(model_name="tts_models/es/mai/glow-tts", language="es"):
    """Probar síntesis con un modelo específico."""
    print("\n" + "=" * 70)
    print(f"Probando modelo: {model_name}")
    print("=" * 70)
    
    try:
        tts = TTS(model_name=model_name, gpu=False)
        print(f"✓ Modelo cargado correctamente")
        
        # Prueba de síntesis
        text = "Soy JARVIS, tu asistente inteligente. Estoy listo para ayudarte." if language == "es" else \
               "I am JARVIS, your intelligent assistant. I am ready to help you."
        
        output_path = "test_voice.wav"
        print(f"\nSintetizando prueba: '{text}'")
        print(f"Guardando en: {output_path}")
        
        tts.tts_to_file(text=text, file_path=output_path)
        
        if os.path.exists(output_path):
            size = os.path.getsize(output_path) / 1024
            print(f"✓ Archivo creado exitosamente ({size:.1f} KB)")
            print(f"  Puedes reproducir: {output_path}")
            return True
        else:
            print("✗ Error: archivo no fue creado")
            return False
    
    except Exception as e:
        print(f"✗ Error al cargar o usar el modelo: {e}")
        print("\nTips:")
        print("  - Algunos modelos requieren descargas grandes (100MB - 1GB)")
        print("  - Primera ejecución descargará el modelo automáticamente")
        print("  - Asegúrate de tener conexión a internet para descargar")
        return False


def recommend_jarvis_voice():
    """Recomendar configuración para voz JARVIS."""
    print("\n" + "=" * 70)
    print("Recomendación para voz JARVIS")
    print("=" * 70)
    
    print("""
Opciones recomendadas (en orden de preferencia):

1. ESPAÑOL PROFESIONAL (Recomendado para compatibilidad):
   - Modelo: tts_models/es/mai/glow-tts
   - Ventaja: Funciona offline completamente
   - Características: Voz clara, natural, profesional
   - Tamaño: ~50-100MB

2. INGLÉS BRITÁNICO (Más cercano a JARVIS original):
   - Modelo: tts_models/en/ljspeech/glow-tts
   - Ventaja: Voz profesional tipo asistente IA
   - Tamaño: ~50-100MB
   - Nota: Habla en inglés

3. MULTILINGUAL (Más flexible pero más pesado):
   - Modelo: tts_models/multilingual/multi-dataset/bark
   - Ventaja: Soporta muchos idiomas y acentos
   - Tamaño: ~10GB (muy grande)
   - No recomendado para computadoras con recursos limitados

SUGERENCIA: Usa la opción 1 (Español) si prefieres compatibilidad local.
            Usa la opción 2 (Inglés) si quieres una voz más "JARVIS-like".
    """)


if __name__ == "__main__":
    list_available_voices()
    recommend_jarvis_voice()
    
    # Preguntar qué modelo usar
    print("\n" + "=" * 70)
    print("NEXT STEP: Elige un modelo y ejecuta test_voices()")
    print("=" * 70)
    print("""
Ejemplo (en Python):
  python -c "from explore_voices import test_voices; test_voices('tts_models/es/mai/glow-tts', 'es')"
    """)
