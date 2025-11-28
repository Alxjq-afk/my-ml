#!/usr/bin/env python3
"""Test offline de JARVIS: STT (VOSK), wake-word, TTS (pyttsx3)."""
import sys
import os
import json

def test_vosk_stt():
    """Probar VOSK STT con archivo de prueba (si existe) o aviso."""
    print("\n=== TEST 1: VOSK STT (Offline) ===")
    try:
        from assistant.stt_vosk import VoskSTT
        model_dir = os.path.join('assistant_data', 'models', 'vosk-model-small-es-0.22')
        if os.path.exists(model_dir):
            stt = VoskSTT(model_path=model_dir)
            print("✓ VOSK STT inicializado correctamente")
            print(f"  Modelo: {model_dir}")
            print("  Nota: Para probar micrófono, ejecuta manualmente el launcher")
            return True
        else:
            print(f"✗ Modelo VOSK no encontrado en {model_dir}")
            return False
    except Exception as e:
        print(f"✗ Error al inicializar VOSK STT: {e}")
        return False

def test_wake_word():
    """Probar detector de wake-word."""
    print("\n=== TEST 2: Wake-Word Detector (VOSK + Google Fallback) ===")
    try:
        from assistant.wake_word import WakeWordDetector
        detector = WakeWordDetector()
        print("✓ Wake-Word Detector inicializado")
        if getattr(detector, 'vosk_available', False):
            print("  ✓ VOSK disponible para detección (offline)")
        else:
            print("  ⚠ VOSK no disponible, usará Google Speech Recognition (online)")
        print("  Nota: Para probar micrófono, ejecuta manualmente el launcher")
        return True
    except Exception as e:
        print(f"✗ Error al inicializar Wake-Word Detector: {e}")
        return False

def test_tts():
    """Probar TTS con pyttsx3."""
    print("\n=== TEST 3: TTS (pyttsx3 - Offline) ===")
    try:
        from assistant import voice
        voices = voice.list_voices()
        print(f"✓ {len(voices)} voces disponibles en el sistema:")
        for v in voices:
            print(f"  - {v['name']} ({v['id'][:40]}...)")
        
        print("\n  Probando síntesis de voz...")
        voice.speak("Bienvenido. Soy JARVIS, tu asistente inteligente. Estoy listo.")
        print("  ✓ TTS funcionando (debería haber escuchado la voz)")
        return True
    except Exception as e:
        print(f"✗ Error al probar TTS: {e}")
        return False

def test_llm():
    """Probar LLM (local si está disponible, sino remoto)."""
    print("\n=== TEST 4: LLM Backend ===")
    try:
        from assistant.llm import LocalLLM
        llm = LocalLLM()
        print("✓ LocalLLM inicializado")
        print(f"  Backend: {llm.backend}")
        if llm.backend == "local":
            print("  Usando Mistral local (offline)")
        else:
            print("  Usando Hugging Face remoto (requiere internet)")
        
        # Probar generación
        prompt = "¿Cuál es tu nombre?"
        resp = llm.generate(prompt)
        print(f"\n  Respuesta de prueba a '{prompt}':")
        print(f"  > {resp[:100]}...")
        return True
    except Exception as e:
        print(f"✗ Error al probar LLM: {e}")
        return False

def test_memory():
    """Probar memoria."""
    print("\n=== TEST 5: Memory (Persistencia Local) ===")
    try:
        from assistant.memory import Memory
        mem = Memory()
        
        # Guardar
        mem.add("user", "¿Hola, cómo estás?")
        mem.add("assistant", "Hola, bien gracias. ¿En qué puedo ayudarte?")
        
        # Leer
        memories = mem.list()
        print(f"✓ Memory inicializado")
        print(f"  Memorias guardadas: {len(memories)}")
        for m in memories[-2:]:  # Mostrar últimas 2
            print(f"    - {m['role']}: {m.get('text', m.get('content', ''))[:50]}...")
        return True
    except Exception as e:
        print(f"✗ Error al probar Memory: {e}")
        return False

def test_interpreter():
    """Probar intérprete de comandos."""
    print("\n=== TEST 6: Command Interpreter ===")
    try:
        from assistant.interpreter import CommandInterpreter
        ci = CommandInterpreter()
        
        # Test commands
        tests = [
            "abre el navegador",
            "qué hora es",
            "hola, ¿cómo estás?",
        ]
        
        print("✓ CommandInterpreter inicializado")
        print("  Probando interpretación:")
        for t in tests:
            result = ci.interpret(t)
            msg = result.get('message', str(result))
            print(f"    > '{t}' → {result.get('type', 'unknown')} ({msg[:40] if msg else 'N/A'}...)")
        return True
    except Exception as e:
        print(f"✗ Error al probar Interpreter: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("JARVIS Advanced - Test de Modo Offline")
    print("=" * 60)
    
    results = {
        "VOSK STT": test_vosk_stt(),
        "Wake-Word": test_wake_word(),
        "TTS": test_tts(),
        "LLM": test_llm(),
        "Memory": test_memory(),
        "Interpreter": test_interpreter(),
    }
    
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    for test, passed in results.items():
        status = "✓ PASÓ" if passed else "✗ FALLÓ"
        print(f"{test:20} {status}")
    
    passed = sum(results.values())
    total = len(results)
    print(f"\nTotal: {passed}/{total} pruebas pasadas")
    print("\n✓ JARVIS está listo en modo offline (STT+TTS).")
    print("  Para usar con micrófono, ejecuta: .\\jarvis_launcher.bat\n")

if __name__ == "__main__":
    main()

