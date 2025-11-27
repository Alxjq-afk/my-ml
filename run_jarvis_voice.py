#!/usr/bin/env python3
"""JARVIS Advanced - CLI con voz (STT → LLM → TTS) y escucha continua."""
import argparse
import sys
import threading
import time
from pathlib import Path

from assistant import config, voice
from assistant.llm import LocalLLM
from assistant.memory import Memory
from assistant.stt import WhisperSTT
from assistant.wake_word import WakeWordDetector
from assistant.interpreter import CommandInterpreter
from assistant.apis import IntegratedAPIs


def main():
    parser = argparse.ArgumentParser(prog="jarvis-voice")
    parser.add_argument("--mode", choices=["cli", "voice", "hybrid"], default="hybrid",
                       help="Modo: 'cli' (texto), 'voice' (voz), 'hybrid' (auto detección)")
    parser.add_argument("--confirm-actions", action="store_true",
                       help="Pedir confirmación antes de ejecutar acciones")
    parser.add_argument("--no-tts", action="store_true",
                       help="Desabilitar síntesis de voz (TTS)")
    parser.add_argument("--stt-model", choices=["tiny", "base", "small", "medium"],
                       default="base",
                       help="Modelo Whisper para STT")
    args = parser.parse_args()

    # Cargar configuración
    config.load_config()
    model_path = config.get("MODEL_PATH")
    
    # Inicializar componentes
    print("🚀 JARVIS Advanced v2.0 - Inicializando...")
    print("=" * 60)
    
    # LLM
    print("📦 Cargando modelo de lenguaje...")
    L = LocalLLM(model_path=model_path)
    
    # Memoria
    print("💾 Inicializando memoria...")
    mem = Memory()
    
    # STT (Speech-to-Text)
    print("🎤 Cargando Whisper STT...")
    stt = WhisperSTT(model_name=args.stt_model, language="es")
    
    # Wake word detector
    print("🔊 Inicializando detección de palabra clave...")
    wake_detector = WakeWordDetector()
    
    # Command interpreter
    CI = CommandInterpreter()
    
    # APIs
    apis = IntegratedAPIs()
    
    # Voice/TTS
    if not args.no_tts:
        print("🔊 Inicializando TTS...")
    
    print("=" * 60)
    print("✓ JARVIS listo")
    print(f"Modo: {args.mode}")
    
    if args.mode in ("voice", "hybrid"):
        print("\n🎙️  Modo voz activado")
        print("Di 'Hey JARVIS' para activar escucha...")
        print("(Escribe 'exit' en terminal para salir)\n")
        voice_loop(stt, wake_detector, L, mem, CI, apis, args, voice)
    else:
        print("\n📝 Modo CLI")
        print("Escribe 'exit' para salir\n")
        cli_loop(L, mem, CI, args, voice)


def cli_loop(llm, memory, interpreter, args, voice_module):
    """Loop CLI tradicional (texto)."""
    while True:
        try:
            txt = input("Tú> ")
        except (KeyboardInterrupt, EOFError):
            print("\n\nAdiós.")
            sys.exit(0)
        
        if not txt.strip():
            continue
        if txt.strip().lower() in ("exit", "quit", "salir"):
            print("Adiós.")
            break
        
        # Interpretar comando
        cmd_result = interpreter.interpret(txt)
        
        if cmd_result["type"] != "conversation":
            # Es un comando → ejecutar
            print(f"🤖 {cmd_result['message']}")
            continue
        
        # Es conversación → pasar al LLM
        prompt = f"Eres JARVIS en español. Responde de forma cortés y proactiva. Usuario: {txt}"
        resp = llm.generate(prompt)
        print(f"JARVIS> {resp}")
        
        # TTS si está habilitado
        if not args.no_tts:
            try:
                t = threading.Thread(target=voice_module.speak, args=(resp,))
                t.daemon = True
                t.start()
            except Exception:
                pass
        
        # Guardar en memoria
        memory.add_memory("user", txt)
        memory.add_memory("assistant", resp)


def voice_loop(stt, wake_detector, llm, memory, interpreter, apis, args, voice_module):
    """Loop con voz - escucha continua."""
    print("🎙️  Escuchando...")
    
    while True:
        try:
            # Esperar palabra clave "Hey JARVIS"
            print("\n🔊 Esperando palabra clave ('Hey JARVIS')...")
            if not wake_detector.detect_wake_word(timeout=30, phrase_time_limit=5):
                print("⏱ No se detectó palabra clave")
                continue
            
            # Palabra clave detectada → grabar comando
            print("\n🎤 Di tu comando...")
            command_text = stt.listen_and_transcribe(duration=5)
            
            if not command_text:
                print("⚠ No se capturó audio")
                continue
            
            print(f"📝 Entendido: '{command_text}'")
            
            # Interpretar comando
            cmd_result = interpreter.interpret(command_text)
            
            if cmd_result["type"] != "conversation":
                # Es un comando → ejecutar
                print(f"⚙️  {cmd_result['message']}")
                
                if args.confirm_actions:
                    try:
                        # Pedir confirmación por voz: "¿Deseas continuar? Di sí o no"
                        voice_module.speak("¿Deseas continuar? Di sí o no")
                        confirmation = stt.listen_and_transcribe(duration=3)
                        if "no" in confirmation.lower():
                            print("Cancelado")
                            continue
                    except Exception:
                        pass
                
                # TODO: Ejecutar comando (executor)
                continue
            
            # Es conversación → pasar al LLM
            print("\n🤖 Procesando...")
            prompt = f"Eres JARVIS en español. Responde de forma cortés y proactiva de manera concisa (máximo 2-3 oraciones). Usuario: {command_text}"
            response = llm.generate(prompt)
            
            print(f"JARVIS> {response}")
            
            # TTS
            if not args.no_tts:
                try:
                    voice_module.speak(response)
                except Exception:
                    pass
            
            # Guardar en memoria
            memory.add_memory("user", command_text)
            memory.add_memory("assistant", response)
        
        except KeyboardInterrupt:
            print("\n\nAdiós.")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")
            continue


if __name__ == "__main__":
    main()
