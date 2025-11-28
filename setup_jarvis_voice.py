#!/usr/bin/env python3
"""
Setup de voz JARVIS con Coqui TTS.

Este script configura la voz JARVIS usando Coqui TTS para mayor calidad offline.
Una vez ejecutado, el launcher usará automáticamente esta voz.
"""
import os
import sys
import json

try:
    from TTS.api import TTS
except ImportError:
    print("❌ TTS (Coqui) no está instalado.")
    print("   Ejecuta: pip install TTS")
    sys.exit(1)


def setup_jarvis_voice():
    """Configurar modelo de TTS para voz JARVIS."""
    print("=" * 70)
    print("SETUP de Voz JARVIS - Coqui TTS")
    print("=" * 70)
    
    # Opciones de modelos
    models_option = {
        "1": {
            "name": "tts_models/es/mai/glow-tts",
            "desc": "Español profesional (Recomendado)",
            "lang": "es",
            "size": "~80MB",
        },
        "2": {
            "name": "tts_models/en/ljspeech/glow-tts",
            "desc": "Inglés profesional (JARVIS-like)",
            "lang": "en",
            "size": "~100MB",
        },
        "3": {
            "name": "tts_models/es/css10/glow-tts",
            "desc": "Español alternativo",
            "lang": "es",
            "size": "~50MB",
        },
    }
    
    print("\nOpciones de voz JARVIS:\n")
    for key, opt in models_option.items():
        print(f"{key}. {opt['desc']}")
        print(f"   Modelo: {opt['name']}")
        print(f"   Tamaño: {opt['size']}\n")
    
    # Seleccionar opción
    choice = input("Elige opción (1-3) [default: 1]: ").strip() or "1"
    if choice not in models_option:
        print("❌ Opción inválida")
        return False
    
    selected = models_option[choice]
    model_name = selected["name"]
    lang = selected["lang"]
    
    print(f"\n🎵 Descargando e inicializando modelo: {model_name}")
    print("   (Primera ejecución descargará el modelo, puede tomar unos minutos...)")
    
    try:
        # Cargar modelo (descarga automáticamente)
        tts = TTS(model_name=model_name, gpu=False, verbose=True)
        print(f"\n✓ Modelo cargado exitosamente")
        
        # Test
        test_text = "Soy JARVIS, tu asistente inteligente. Estoy listo." if lang == "es" else \
                    "I am JARVIS, your intelligent assistant. I am ready."
        
        print(f"\n🔊 Probando síntesis: '{test_text}'")
        output_path = "test_jarvis_voice.wav"
        tts.tts_to_file(text=test_text, file_path=output_path)
        
        if os.path.exists(output_path):
            size = os.path.getsize(output_path) / 1024
            print(f"✓ Archivo de prueba creado: {output_path} ({size:.1f}KB)")
            print("\n📝 Puedes reproducir el archivo para escuchar la voz")
        
        # Guardar configuración
        config_path = "assistant_data/tts_config.json"
        os.makedirs("assistant_data", exist_ok=True)
        
        config = {
            "engine": "coqui",
            "model": model_name,
            "language": lang,
            "use_gpu": False,
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n✓ Configuración guardada en: {config_path}")
        print("✓ El launcher ahora usará automáticamente Coqui TTS con esta voz JARVIS")
        return True
    
    except Exception as e:
        print(f"❌ Error al configurar voz: {e}")
        return False


if __name__ == "__main__":
    success = setup_jarvis_voice()
    sys.exit(0 if success else 1)
