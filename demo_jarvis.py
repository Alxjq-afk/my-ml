#!/usr/bin/env python3
"""Demo rápida de JARVIS - Prueba de funcionalidades."""
import sys
from assistant import config, voice
from assistant.llm import LocalLLM
from assistant.interpreter import CommandInterpreter
from assistant.apis import IntegratedAPIs


def demo():
    """Demo interactiva de JARVIS."""
    print("=" * 70)
    print("🤖 JARVIS Advanced v2.0 - Demo Interactiva")
    print("=" * 70)
    
    # Cargar configuración
    config.load_config()
    model_path = config.get("MODEL_PATH")
    
    # Inicializar componentes
    print("\n📦 Inicializando componentes...")
    L = LocalLLM(model_path=model_path)
    CI = CommandInterpreter()
    apis = IntegratedAPIs()
    
    print("✓ JARVIS listo\n")
    
    # Menu
    while True:
        print("\n" + "-" * 70)
        print("Opciones:")
        print("  1. Probar comandos naturales (exec, open, volume)")
        print("  2. Probar interpretador de comandos")
        print("  3. Ver hora y fecha")
        print("  4. Búsqueda web")
        print("  5. Conversación con IA")
        print("  6. Salir")
        print("-" * 70)
        
        choice = input("Selecciona opción (1-6): ").strip()
        
        if choice == "1":
            demo_commands(CI)
        elif choice == "2":
            demo_interpreter(CI)
        elif choice == "3":
            demo_time(apis)
        elif choice == "4":
            demo_search(apis)
        elif choice == "5":
            demo_conversation(L)
        elif choice == "6":
            print("\n👋 Adiós!")
            sys.exit(0)
        else:
            print("❌ Opción no válida")


def demo_commands(interpreter):
    """Demo de comandos naturales."""
    print("\n=== Demo: Comandos Naturales ===")
    print("(Los comandos se interpretan pero no se ejecutan realmente)\n")
    
    commands = [
        "abre notepad",
        "ejecuta dir C:\\",
        "sube volumen a 80",
        "baja volumen",
        "envía un correo"
    ]
    
    for cmd in commands:
        result = interpreter.interpret(cmd)
        print(f"📝 '{cmd}'")
        print(f"   → Tipo: {result['type']}")
        print(f"   → {result['message']}")
        print()


def demo_interpreter(interpreter):
    """Demo interactivo del interpretador."""
    print("\n=== Demo: Interpretador de Comandos ===")
    print("Ingresa comandos naturales (ej: 'abre explorer', 'sube volumen a 50')")
    print("(Escribe 'back' para volver)\n")
    
    while True:
        cmd = input("Comando> ").strip()
        if cmd.lower() == "back":
            break
        
        result = interpreter.interpret(cmd)
        print(f"  Tipo: {result['type']}")
        print(f"  Mensaje: {result['message']}")
        if result['type'] != 'conversation':
            for k, v in result.items():
                if k not in ['type', 'message', 'success']:
                    print(f"  {k}: {v}")
        print()


def demo_time(apis):
    """Demo de hora y fecha."""
    print("\n=== Demo: Hora y Fecha ===")
    print(f"Hora actual: {apis.get_time()}")
    print(f"Fecha actual: {apis.get_date()}")
    print(f"Fecha/Hora: {apis.get_datetime()}")


def demo_search(apis):
    """Demo de búsqueda web."""
    print("\n=== Demo: Búsqueda Web ===")
    query = input("¿Qué deseas buscar? ").strip()
    
    if not query:
        print("Búsqueda vacía")
        return
    
    print(f"\nBuscando '{query}'...")
    result = apis.web_search(query)
    
    if "abstract" in result and result["abstract"]:
        print(f"\n📄 Resumen:\n{result['abstract'][:300]}...\n")
    
    if "results" in result and result["results"]:
        print("🔗 Primeros resultados:")
        for i, r in enumerate(result["results"][:3], 1):
            print(f"  {i}. {r.get('title', 'Sin título')}")
            print(f"     {r.get('url', '')}")


def demo_conversation(llm):
    """Demo de conversación con IA."""
    print("\n=== Demo: Conversación con IA ===")
    print("(Escribe 'back' para volver)\n")
    
    while True:
        user_input = input("Tú> ").strip()
        if user_input.lower() == "back":
            break
        
        if not user_input:
            continue
        
        prompt = f"Eres JARVIS, un asistente inteligente en español. Responde de forma cortés y concisa. Usuario: {user_input}"
        response = llm.generate(prompt, max_tokens=150)
        
        print(f"JARVIS> {response}\n")


if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\n\n👋 Adiós!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
