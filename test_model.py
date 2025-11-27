#!/usr/bin/env python3
"""Test script para verificar que el modelo local y llama_cpp funcionan."""
import os
import sys
from pathlib import Path

# Cargar config
sys.path.insert(0, str(Path(__file__).parent))
from assistant import config, llm

config.load_config()
model_path = config.get("MODEL_PATH")

print(f"MODEL_PATH configurado: {model_path}")
if model_path and os.path.exists(model_path):
    print(f"Archivo encontrado, tamaño: {os.path.getsize(model_path) / (1024**3):.2f} GB")
    print("Cargando modelo (puede tomar 10-30 segundos)...")
    L = llm.LocalLLM(model_path=model_path)
    if L.available:
        print("✓ Modelo cargado exitosamente.")
        print("\nGenerando respuesta de prueba...")
        prompt = "Eres un asistente útil en español. Responde brevemente: ¿Cuál es la capital de Francia?"
        resp = L.generate(prompt, max_tokens=100)
        print(f"Respuesta: {resp}")
    else:
        print("✗ Fallo al cargar modelo con llama_cpp.")
else:
    if not model_path:
        print("✗ MODEL_PATH no está configurado en .env")
    else:
        print(f"✗ Archivo no encontrado: {model_path}")
        print("Por favor, espera a que la descarga se complete o verifica la ruta.")
