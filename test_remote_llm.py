#!/usr/bin/env python3
"""Test rápido del backend remoto (Hugging Face)."""
import os
import sys

# Asegurar que estamos en el directorio correcto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Cargar variables de .env
from assistant import config
config.load_config()

from assistant.llm import LocalLLM

L = LocalLLM()
print(f"Backend detectado: {L.backend}")
print(f"Disponible: {L.available}")

if L.backend == "remote":
    print("\n✓ RemoteLLM configurado correctamente.")
    print("\nGenerando respuesta vía Hugging Face API...")
    prompt = "Hola, ¿cómo estás?"
    resp = L.generate(prompt, max_tokens=50)
    print(f"Prompt: {prompt}")
    print(f"Respuesta: {resp}")
elif L.backend == "llama_cpp":
    print("\n✓ Backend local (llama_cpp) disponible.")
else:
    print("\n✗ Sin backend remoto ni local. Usando fallback canned.")
    resp = L.generate("Hola")
    print(f"Respuesta: {resp}")
