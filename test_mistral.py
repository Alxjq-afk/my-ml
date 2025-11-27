"""Test del modelo Mistral 7B local."""
import sys
import time
from assistant import config
from assistant.llm import LocalLLM


def test_mistral_local():
    """Test de Mistral 7B local."""
    print("=== Test de Mistral 7B (LocalLLM) ===\n")
    
    config.load_config()
    model_path = config.get("MODEL_PATH")
    
    print(f"Modelo configurado: {model_path}")
    print("Cargando...")
    
    L = LocalLLM(model_path=model_path)
    
    if not L.available:
        print("❌ No se pudo cargar el modelo")
        return False
    
    print(f"✓ Backend activo: {L.backend}")
    print()
    
    # Test prompts
    test_cases = [
        ("Hola, ¿cómo estás?", "Saludos"),
        ("¿Cuál es 2 + 2?", "Matemática simple"),
        ("¿Quién es Albert Einstein?", "Conocimiento general"),
        ("¿Cuál es la capital de España?", "Geografía"),
    ]
    
    for prompt, description in test_cases:
        print(f"📝 Test: {description}")
        print(f"   Entrada: '{prompt}'")
        print(f"   Generando...", end="", flush=True)
        
        start = time.time()
        response = L.generate(prompt, max_tokens=128)
        elapsed = time.time() - start
        
        print(f" ({elapsed:.2f}s)")
        print(f"   Salida: '{response[:100]}...'")
        print()
    
    return True


if __name__ == "__main__":
    success = test_mistral_local()
    if success:
        print("✓ Test completado exitosamente")
        sys.exit(0)
    else:
        print("❌ Test fallido")
        sys.exit(1)
