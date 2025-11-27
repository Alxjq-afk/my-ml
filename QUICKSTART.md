# 🚀 JARVIS Advanced v2.0 - Quick Start

## Inicio Rápido (30 segundos)

### Opción 1: Script Interactivo (Recomendado)
```bash
# Windows
jarvis.bat

# O si no funciona:
python run_jarvis_voice.py
```

### Opción 2: Línea de Comandos
```bash
# Modo texto (CLI)
python run_jarvis_voice.py --mode cli

# Modo voz (Voice)
python run_jarvis_voice.py --mode voice

# Demo interactiva
python demo_jarvis.py

# Demo rápida
python demo_quick.py
```

---

## 💬 Ejemplos de Comandos

### Comandos del Sistema
```
"abre notepad"              → Abre Notepad
"abre explorer"             → Abre File Explorer
"ejecuta dir C:\"           → Ejecuta comando dir
"sube volumen a 80"         → Ajusta volumen a 80%
"baja volumen"              → Baja volumen 10%
"envía un correo"           → Abre panel de envío de email
```

### Preguntas Normales
```
"¿Qué hora es?"             → JARVIS responde la hora
"¿Cuál es la capital de España?"   → Busca la respuesta
"Dime un chiste"            → Genera una respuesta IA
"¿Cuánto es 2 + 2?"         → Calcula (resultado: 4)
```

### Búsquedas
```
"Busca información sobre Python"    → Busca en web
"¿Quién fue Albert Einstein?"       → Busca biografia
```

---

## 🎯 Modos Disponibles

### CLI Mode (Texto)
```
Ideal para:
- Desarrollo/debugging
- Sin micrófono
- Entorno ruidoso

Comando:
python run_jarvis_voice.py --mode cli
```

### Voice Mode (Voz)
```
Ideal para:
- Hands-free control
- Interacción natural
- Escucha continua

Comando:
python run_jarvis_voice.py --mode voice

Uso:
1. Escucha esperando "Hey JARVIS"
2. Di tu comando o pregunta
3. JARVIS responde por voz
```

### Hybrid Mode (Recomendado)
```
Ideal para:
- El mejor de ambos mundos
- Auto-detecta CLI o voz

Comando:
python run_jarvis_voice.py
```

---

## ⚙️ Opciones Avanzadas

```bash
# Cambiar modelo STT (recomendado para latencia baja)
python run_jarvis_voice.py --stt-model tiny

# Pedir confirmación antes de ejecutar comandos
python run_jarvis_voice.py --confirm-actions

# Desabilitar síntesis de voz
python run_jarvis_voice.py --no-tts

# Combinaciones
python run_jarvis_voice.py --mode voice --stt-model small --confirm-actions
```

Opciones de STT:
- `tiny` - Muy rápido, menos preciso
- `base` - Balance (recomendado)
- `small` - Más preciso, más lento
- `medium` - Muy preciso, muy lento

---

## 🔧 Troubleshooting

### "No escucho nada / Micrófono no funciona"
```bash
# Verificar dispositivos de audio disponibles
python -c "import sounddevice as sd; print(sd.query_devices())"
```

### "Whisper es muy lento"
→ Usa `--stt-model tiny` para grabaciones más rápidas

### "No detecta 'Hey JARVIS'"
→ Habla más claro y en español
→ Acerca el micrófono
→ Verifica conexión a internet (Google Speech API)

### "Error de token HF"
→ El token en `.env` es público, fue revocado
→ Genera un nuevo token en https://huggingface.co/settings/tokens

### "AttributeError: llama-cpp-python"
→ Normal, se usa HF API como fallback automáticamente
→ Todo funciona sin problema

---

## 📊 Información del Sistema

Implementado en:
- **OS**: Windows 10/11
- **Python**: 3.13 (venv .venv311)
- **LLM Backend**: Hugging Face Inference API (distilgpt2)
- **STT**: OpenAI Whisper
- **TTS**: pyttsx3
- **Tamaño modelo Mistral**: 4.37 GB (opcional, local)

---

## 🎬 Ejemplos de Sesiones

### Sesión 1: Comandos del Sistema
```
🎤 Escuchando...
📝 Detectado: "abre notepad"
⚙️  Abriendo: notepad
✓ Notepad abierto

🎤 Escuchando...
📝 Detectado: "sube volumen a 75"
⚙️  Ajustando volumen a 75
✓ Volumen ajustado
```

### Sesión 2: Conversación
```
🎤 Escuchando...
📝 Detectado: "¿qué hora es?"
🤖 Procesando...
JARVIS> Son las 17:39:21 del 27 de Noviembre de 2025.
🔊 [Audio de respuesta]
```

### Sesión 3: Búsqueda Web
```
🎤 Escuchando...
📝 Detectado: "quién fue Einstein"
🤖 Procesando...
JARVIS> Albert Einstein fue un físico teórico alemán...
🔊 [Audio de respuesta]
```

---

## 📚 Documentación Completa

Para más detalles, ver:
- **JARVIS_ADVANCED.md** - Arquitectura y características
- **JARVIS_USAGE.md** - Guía de uso original
- **IMPLEMENTATION_SUMMARY.md** - Resumen técnico
- **README.md** - Overview del proyecto

---

## ❓ Preguntas Frecuentes

**P: ¿Funciona sin internet?**
R: La mayoría sí (Whisper local, comandos). Búsquedas web requieren internet.

**P: ¿Necesito compilar llama-cpp-python?**
R: No, HF API funciona como fallback automáticamente.

**P: ¿Cuánto tarda en responder?**
R: ~15-20 segundos por ciclo completo (STT → LLM → TTS).

**P: ¿Puedo entrenar un modelo propio?**
R: Sí, ver `train.py` para entrenamiento ML.

**P: ¿Cuáles son los requisitos de hardware?**
R: CPU 4-core, 4GB RAM mínimo. GPU opcional para Mistral local.

**P: ¿Es seguro usar mi token HF?**
R: Sí, están revocados públicamente. Genera nuevos en https://huggingface.co/settings/tokens

---

## 🚀 Próximas Mejoras

- [ ] Soporte para GPU con CUDA
- [ ] Más comandos naturales
- [ ] Integración con calendario
- [ ] Smart home control
- [ ] Múltiples idiomas

---

## 🆘 Soporte

Si encuentras problemas:
1. Revisa el troubleshooting arriba
2. Consulta JARVIS_ADVANCED.md
3. Crea un issue en GitHub

---

**Versión**: 2.0 (Advanced Voice)  
**Última actualización**: 27 Noviembre 2025  
**Estado**: ✅ Producción-Ready

**¡Disfruta de JARVIS! 🤖**
