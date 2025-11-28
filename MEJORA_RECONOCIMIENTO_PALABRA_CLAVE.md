# Mejora de Reconocimiento de Palabra Clave - JARVIS

## Resumen del Problema
Usuario reportó: **"estoy viendo que da palabras que no son"** durante el reconocimiento de "JARVIS".

### Causa Raíz
- **VOSK STT** (Speech-to-Text offline) es un modelo pequeño en español que puede cometer errores de transcripción
- Al decir "jarvis", VOSK podría transcribir variaciones como: "jarmis", "jarfis", "garvis", "harvis"
- La detección original usaba búsqueda substring simple: `if wake_word in text_lower`
- Esta lógica no toleraba ningún error de transcripción

## Solución Implementada: Fuzzy Matching

Se mejoró `assistant/wake_word.py` con **fuzzy matching** usando `difflib.SequenceMatcher` (stdlib Python, sin dependencias nuevas).

### Cambios Principales

#### 1. Nueva función: `_is_similar()`
```python
def _is_similar(a, b, threshold=0.75):
    """Comparar similitud entre dos strings (fuzzy matching)."""
    ratio = SequenceMatcher(None, a.lower(), b.lower()).ratio()
    return ratio >= threshold
```

- Compara similitud de caracteres entre dos strings
- Umbral: 70% de similitud mínima (tolera ~30% de diferencia)
- Sin diferenciación entre mayúsculas/minúsculas

#### 2. Método mejorado: `_contains_wake_word()`
Ahora hace búsqueda en dos fases:
1. **Búsqueda exacta** (rápida): busca substring literal "jarvis" en el texto
2. **Búsqueda fuzzy** (tolerante): compara similitud palabra por palabra

```python
def _contains_wake_word(self, text):
    # Búsqueda exacta (rápida)
    for wake_word in self.wake_words:
        if wake_word in text_lower:
            return True, wake_word
    
    # Búsqueda fuzzy (tolera pequeños errores)
    for wake_word in self.wake_words:
        if _is_similar(text_lower, wake_word, self.similarity_threshold):
            return True, wake_word
        for word in text_lower.split():
            if _is_similar(word, wake_word, self.similarity_threshold):
                return True, wake_word
    
    return False, None
```

#### 3. Palabras clave soportadas
- "jarvis" ✓
- "oye jarvis" ✓
- "hey jarvis" ✓ (agregado para compatibilidad)

### Variaciones Detectadas Correctamente

✅ **Variaciones fonéticas (1 carácter diferente)**
- "jarmis" (v→m)
- "jarfis" (v→f)
- "garvis" (j→g)
- "harvis" (j→h)
- "jarwis" (v→w)

✅ **Con contexto**
- "di jarvis ahora"
- "oye jarvis encende la luz"
- "hey jarmis por favor"

✅ **Exactos**
- "jarvis" (lowercase)
- "JARVIS" (uppercase)
- "oye jarvis"
- "hey jarvis"

❌ **Rechazados correctamente** (no similares)
- "hola"
- "luis" (aunque suena similar, 40% similitud)
- "java"
- "carlos"

## Pruebas Implementadas

### Test 1: `test_fuzzy_wake_word.py`
- 8 tests para función `_is_similar()` → **8/8 PASADOS**
- 17 tests para detección con contexto → **17/17 PASADOS**

**Resultados:**
```
Función _is_similar: 8/8 tests pasados
Detección con contexto: 17/17 tests pasados
Total: 25/25 tests pasados
```

### Test 2: `test_offline_mode.py` (existentes)
- 6 tests de modo offline → **6/6 PASADOS** (sin cambios)

**Verificado:**
- VOSK STT inicializa correctamente
- Wake-Word Detector con fuzzy matching inicializa correctamente
- TTS (pyttsx3) sigue funcionando
- LLM backend disponible
- Memory persistencia
- Interpreter de comandos

## Impacto

| Aspecto | Antes | Después |
|---------|-------|---------|
| Tolerancia a errores | 0% (exacta) | ~30% (fuzzy) |
| Variaciones detectadas | "jarvis", "oye jarvis" | "jarvis", "jarmis", "garvis", "harvis", etc. + contexto |
| Dependencias nuevas | - | 0 (usa difflib stdlib) |
| Performance | O(n) | O(n*m) pero con búsqueda exacta primero |

## Uso

El usuario no necesita hacer nada especial. Cuando diga "JARVIS" u "Oye JARVIS":
- Si VOSK transcribe exactamente → detección inmediata
- Si VOSK transcribe con error pequeño (1-2 caracteres) → detección fuzzy
- Si no es similar → rechaza y espera nuevo intento

Ejecutar launcher como siempre:
```powershell
.\jarvis_launcher.bat
```

## Commits
- `25cd626` - Mejorar reconocimiento de palabra clave con fuzzy matching
- Test nuevo: `test_fuzzy_wake_word.py` creado
- Archivo modificado: `assistant/wake_word.py`

## Siguientes Pasos Opcionales (No Implementados)

1. **Phonetic Matching (Soundex/Metaphone)** - más sofisticado pero requiere dependencia externa
2. **Confidence Scoring** - si VOSK devuelve múltiples hipótesis, elegir la más probable
3. **Machine Learning** - entrenar un modelo específico para detección de "jarvis"
4. **Accent Normalization** - "javiz", "harviz" (se soporta parcialmente con fuzzy)

---

**Estado:** ✅ COMPLETADO Y TESTEADO
