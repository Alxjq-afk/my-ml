#!/usr/bin/env python3
"""Test de fuzzy matching en detección de palabra clave."""
import sys
import os

def test_fuzzy_matching():
    """Probar que fuzzy matching detecta variaciones de 'jarvis'."""
    print("\n=== TEST: Fuzzy Matching en Wake-Word Detection ===\n")
    
    from assistant.wake_word import WakeWordDetector, _is_similar
    
    detector = WakeWordDetector()
    
    # Test casos: (texto, debe_detectar, descripción)
    test_cases = [
        # Exactos
        ("jarvis", True, "Exacto: 'jarvis'"),
        ("JARVIS", True, "Exacto mayúsculas: 'JARVIS'"),
        ("oye jarvis", True, "Exacto: 'oye jarvis'"),
        ("hey jarvis", True, "Exacto: 'hey jarvis'"),
        
        # Variaciones similares (fuzzy)
        ("jarmis", True, "Variación fonética: 'jarmis'"),
        ("jarfis", True, "Variación fonética: 'jarfis'"),
        ("garvis", True, "Variación fonética: 'garvis'"),
        ("harvis", True, "Variación similar: 'harvis'"),
        ("jarwis", True, "Variación similar: 'jarwis'"),
        
        # Casos con contexto
        ("di jarvis ahora", True, "Contexto: 'di jarvis ahora'"),
        ("oye jarvis encende la luz", True, "Contexto: 'oye jarvis encende...'"),
        ("hey jarmis por favor", True, "Contexto con variación: 'hey jarmis...'"),
        
        # Casos negativos (NO deben detectar)
        ("hola", False, "No similar: 'hola'"),
        ("luis", False, "No similar (pero sí pronunciación): 'luis'"),
        ("java", False, "No similar: 'java'"),
        ("carlos", False, "No similar: 'carlos'"),
        ("", False, "Vacío: ''"),
    ]
    
    print(f"Palabras clave configuradas: {detector.wake_words}")
    print(f"Umbral de similitud: {detector.similarity_threshold}\n")
    
    passed = 0
    failed = 0
    
    for text, expected, description in test_cases:
        found, matched_word = detector._contains_wake_word(text)
        result = "✓" if found == expected else "✗"
        status = "DETECTADO" if found else "NO detectado"
        
        if found == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"{result} {description:40} → {status}")
        if found:
            print(f"   (Coincidió con: '{matched_word}')")
    
    print(f"\n{'='*60}")
    print(f"Resultados: {passed} pasado, {failed} fallido")
    print(f"Total: {passed}/{passed + failed}")
    
    return failed == 0

def test_similarity_function():
    """Probar función _is_similar directamente."""
    print("\n=== TEST: Función _is_similar (Fuzzy Matching) ===\n")
    
    from assistant.wake_word import _is_similar
    
    test_pairs = [
        # (word1, word2, threshold, should_match, description)
        ("jarvis", "jarvis", 0.70, True, "Idéntico"),
        ("jarvis", "jarmis", 0.70, True, "1 char diferente"),
        ("jarvis", "jarfis", 0.70, True, "1 char diferente"),
        ("jarvis", "garvis", 0.70, True, "1 char diferente (inicio)"),
        ("jarvis", "harvis", 0.70, True, "1 char diferente (inicio)"),
        ("jarvis", "hola", 0.70, False, "Totalmente diferente"),
        ("jarvis", "java", 0.70, False, "Solo 2 caracteres en común"),
        ("oye jarvis", "oye jarmis", 0.70, True, "Frase con variación"),
    ]
    
    print(f"Umbral por defecto: 0.70\n")
    
    passed = 0
    for word1, word2, threshold, expected, description in test_pairs:
        result = _is_similar(word1, word2, threshold)
        check = "✓" if result == expected else "✗"
        
        if result == expected:
            passed += 1
        
        similarity = int((0.75 * 100) if result else (0.50 * 100))  # aproximado
        print(f"{check} {description:30} | '{word1}' vs '{word2}' → {result}")
    
    print(f"\n{'='*60}")
    print(f"Resultados: {passed}/{len(test_pairs)} tests pasados")
    
    return passed == len(test_pairs)

def main():
    print("\n" + "=" * 60)
    print("JARVIS - Test de Fuzzy Matching para Wake-Word")
    print("=" * 60)
    
    test1_passed = test_similarity_function()
    test2_passed = test_fuzzy_matching()
    
    print("\n" + "=" * 60)
    print("RESUMEN GENERAL")
    print("=" * 60)
    
    if test1_passed and test2_passed:
        print("✓ TODOS LOS TESTS PASARON")
        print("\nMejoras implementadas:")
        print("  ✓ Fuzzy matching con difflib.SequenceMatcher")
        print("  ✓ Tolerancia a ~30% de diferencia en caracteres")
        print("  ✓ Detección de palabras similares en texto")
        print("  ✓ Soporte para variaciones fonéticas (jarmis, garvis, harvis)")
        return 0
    else:
        print("✗ ALGUNOS TESTS FALLARON")
        return 1

if __name__ == "__main__":
    sys.exit(main())
