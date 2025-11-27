"""Test de APIs integradas."""
import sys
from assistant.apis import IntegratedAPIs


def test_datetime():
    """Test de hora y fecha."""
    print("=== Test: Hora y Fecha ===")
    api = IntegratedAPIs()
    
    print(f"Hora: {api.get_time()}")
    print(f"Fecha: {api.get_date()}")
    print(f"Fecha/Hora completa: {api.get_datetime()}")
    print("✓ Hora y fecha OK\n")


def test_web_search():
    """Test de búsqueda web."""
    print("=== Test: Búsqueda Web ===")
    api = IntegratedAPIs()
    
    result = api.web_search("Python programming")
    print(f"Búsqueda: 'Python programming'")
    if "abstract" in result and result["abstract"]:
        print(f"Resumen: {result['abstract'][:150]}...")
    if "answer" in result and result["answer"]:
        print(f"Respuesta rápida: {result['answer']}")
    if "results" in result:
        print(f"Primeros resultados:")
        for i, r in enumerate(result["results"][:2], 1):
            print(f"  {i}. {r.get('title', 'Sin título')}")
    print("✓ Búsqueda web OK\n")


def test_math():
    """Test de cálculos."""
    print("=== Test: Cálculos ===")
    api = IntegratedAPIs()
    
    tests = [
        ("2 + 2", 4),
        ("10 * 5", 50),
        ("sqrt(16)", 4),
        ("pi", 3.14159),
    ]
    
    for expr, expected in tests:
        result = api.calculate(expr)
        status = "✓" if result and abs(result - expected) < 0.1 else "❌"
        print(f"{status} {expr} = {result}")
    print()


def test_system_info():
    """Test de info del sistema."""
    print("=== Test: Info del Sistema ===")
    api = IntegratedAPIs()
    
    try:
        info = api.get_system_info()
        print(f"OS: {info['system']} {info['version']}")
        print(f"CPU: {info['cpu_percent']}%")
        print(f"Memoria: {info['memory_percent']}%")
        print(f"Disco: {info['disk_usage']}%")
        print("✓ Info del sistema OK\n")
    except Exception as e:
        print(f"⚠ Error: {e}\n")


if __name__ == "__main__":
    print("=== TESTS DE APIs INTEGRADAS ===\n")
    
    test_datetime()
    test_math()
    test_system_info()
    test_web_search()
    
    print("✓ Todos los tests completados")
