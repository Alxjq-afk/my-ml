"""Test de STT con Whisper - Demo interactivo."""
import sys
from assistant.stt import WhisperSTT


def test_stt_interactive():
    """Test interactivo de Whisper."""
    print("=== Test de Whisper STT ===\n")
    
    # Usar modelo tiny para test rápido
    stt = WhisperSTT(model_name="tiny", language="es")
    print()
    
    # Probar 2 grabaciones
    for i in range(2):
        print(f"\n--- Grabación {i+1} ---")
        print("Di algo en español (máximo 5 segundos)...")
        text = stt.listen_and_transcribe(duration=5)
        
        if text:
            print(f"✓ Transcrito: '{text}'")
        else:
            print("⚠ No se capturó audio")
    
    print("\n✓ Test completado")


if __name__ == "__main__":
    try:
        test_stt_interactive()
    except KeyboardInterrupt:
        print("\n\nInterrumpido por usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
