#!/usr/bin/env python3
"""
Demo interactiva: Probar fuzzy matching en wake-word con entrada del usuario.
Permite escribir diferentes variaciones de 'jarvis' para ver si se detectan.
"""
import sys
import os

def interactive_demo():
    """Demo interactiva de fuzzy matching."""
    from assistant.wake_word import WakeWordDetector
    
    detector = WakeWordDetector()
    
    print("\n" + "=" * 70)
    print("JARVIS - Demo Interactiva de Fuzzy Matching en Palabra Clave")
    print("=" * 70)
    print("\nEsta demo simula lo que pasaría si VOSK transcribiera tu voz de")
    print("diferentes formas. Puedes escribir lo que VOSK transcribiera para")
    print("ver si la palabra clave es detectada correctamente.\n")
    
    print(f"Palabras clave configuradas: {detector.wake_words}")
    print(f"Umbral de similitud: {detector.similarity_threshold * 100:.0f}%\n")
    
    example_inputs = [
        "jarvis",
        "jarmis",
        "garvis",
        "harvis",
        "oye jarvis",
        "hey jarmis",
        "di jarvis ahora",
        "hola",
        "luis",
    ]
    
    print("Ejemplos que puedes probar:")
    for i, ex in enumerate(example_inputs, 1):
        print(f"  {i:2}. '{ex}'")
    
    print("\nEscribe 'salir' para terminar.\n")
    
    attempt = 0
    while True:
        try:
            text = input("📝 Escribe lo que VOSK transcribió: ").strip()
            
            if text.lower() in ['salir', 'exit', 'quit', 'q']:
                print("\n✓ Demo terminada")
                break
            
            if not text:
                print("⚠ Por favor, escribe algo\n")
                continue
            
            attempt += 1
            found, matched_word = detector._contains_wake_word(text)
            
            if found:
                print(f"✓ DETECTADO: Coincidió con '{matched_word}'")
            else:
                print(f"✗ NO DETECTADO: No es palabra clave")
                print(f"  (Esperaba: {detector.wake_words})")
            
            # Mostrar análisis detallado
            print("\n  Análisis detallado:")
            from assistant.wake_word import _is_similar
            
            text_lower = text.lower().strip()
            
            # Búsqueda exacta
            exact_found = any(ww in text_lower for ww in detector.wake_words)
            print(f"  - Búsqueda exacta (substring): {'✓' if exact_found else '✗'}")
            
            # Búsqueda fuzzy
            print(f"  - Búsqueda fuzzy (similitud):")
            for wake_word in detector.wake_words:
                # Palabras completas
                sim = int(_is_similar(text_lower, wake_word, 0.0) * 100)  # Get ratio
                from difflib import SequenceMatcher
                ratio = SequenceMatcher(None, text_lower, wake_word).ratio()
                print(f"    '{text_lower}' vs '{wake_word}': {ratio*100:.0f}% {'✓' if ratio >= detector.similarity_threshold else '✗'}")
                
                # Palabras individuales en el texto
                for word in text_lower.split():
                    if len(word) > 2:  # Solo palabras > 2 caracteres
                        ratio = SequenceMatcher(None, word, wake_word).ratio()
                        print(f"    '{word}' vs '{wake_word}': {ratio*100:.0f}% {'✓' if ratio >= detector.similarity_threshold else '✗'}")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n⏹ Demo interrumpida por el usuario")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}\n")

def batch_test():
    """Ejecutar test en lote con ejemplos predefinidos."""
    from assistant.wake_word import WakeWordDetector, _is_similar
    
    detector = WakeWordDetector()
    
    print("\n" + "=" * 70)
    print("JARVIS - Batch Test de Fuzzy Matching")
    print("=" * 70 + "\n")
    
    test_cases = {
        "Variaciones exactas": [
            ("jarvis", True),
            ("JARVIS", True),
            ("oye jarvis", True),
            ("hey jarvis", True),
        ],
        "Variaciones con 1 error (fuzzy)": [
            ("jarmis", True),   # v→m
            ("jarfis", True),   # v→f
            ("garvis", True),   # j→g
            ("harvis", True),   # j→h
            ("jarwis", True),   # v→w
        ],
        "Con contexto": [
            ("di jarvis ahora", True),
            ("oye jarvis encende la luz", True),
            ("hey jarmis por favor", True),
        ],
        "Rechazados (no similares)": [
            ("hola", False),
            ("luis", False),
            ("java", False),
            ("carlos", False),
        ],
    }
    
    total_tests = 0
    passed_tests = 0
    
    for category, cases in test_cases.items():
        print(f"\n{category}:")
        print("-" * 70)
        
        for text, should_detect in cases:
            found, matched_word = detector._contains_wake_word(text)
            test_passed = found == should_detect
            
            total_tests += 1
            if test_passed:
                passed_tests += 1
            
            status = "✓" if test_passed else "✗"
            result = "DETECTADO" if found else "NO detectado"
            
            print(f"{status} '{text:30}' → {result:15} {'(Esperado)' if test_passed else '(ERROR!)'}")
    
    print("\n" + "=" * 70)
    print(f"RESULTADOS: {passed_tests}/{total_tests} tests pasados")
    print("=" * 70)
    
    return passed_tests == total_tests

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--batch':
        success = batch_test()
        sys.exit(0 if success else 1)
    else:
        interactive_demo()
        sys.exit(0)

if __name__ == "__main__":
    main()
