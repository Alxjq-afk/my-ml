"""Wrapper para modelo local (llama_cpp) con fallback remoto (Hugging Face).

Intenta cargar `llama_cpp` si está disponible y `MODEL_PATH` en `.env`.
Si no hay modelo local, intenta usar RemoteLLM (Hugging Face API) si está configurado.
Si tampoco, devuelve respuestas de fallback instructivas.
"""
from typing import Optional
import os
import json
import requests


class RemoteLLM:
    """Cliente mínimo para Hugging Face Inference API.

    Usa las variables de entorno:
    - REMOTE_PROVIDER: 'hf' para Hugging Face (por ahora único soportado)
    - HF_API_KEY: token de Hugging Face
    - REMOTE_MODEL: id del modelo en HF (p.ej. 'meta-llama/Llama-2-7b-chat')
    """

    def __init__(self):
        self.provider = os.getenv("REMOTE_PROVIDER", "hf")
        self.api_key = os.getenv("HF_API_KEY")
        self.model = os.getenv("REMOTE_MODEL")

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        if self.provider != "hf":
            return "[RemoteLLM] proveedor remoto no configurado (solo 'hf' soportado)."

        if not self.api_key or not self.model:
            return "[RemoteLLM] falta HF_API_KEY o REMOTE_MODEL en el entorno."

        url = f"https://api-inference.huggingface.co/models/{self.model}"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_tokens}}
        try:
            resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
            resp.raise_for_status()
            data = resp.json()
            # Manejar formatos: {'generated_text': '...'} o list of dicts
            if isinstance(data, dict) and "generated_text" in data:
                return data["generated_text"].strip()
            if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
                return data[0]["generated_text"].strip()
            # Algunos endpoints devuelven texto plano
            if isinstance(data, str):
                return data.strip()
            return str(data)
        except Exception as e:
            return f"[RemoteLLM error] {e}"


class LocalLLM:
    """Interfaz unificada: intenta usar un backend local (`llama_cpp`) y si no está
    disponible intenta un backend remoto configurado, o devuelve respuestas de fallback.
    """

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or os.getenv("MODEL_PATH")
        self.backend = None
        self.available = False
        self.llm = None

        # Intentar backend local (llama_cpp)
        try:
            from llama_cpp import Llama

            if self.model_path and os.path.exists(self.model_path):
                self.llm = Llama(model_path=self.model_path)
                self.available = True
                self.backend = "llama_cpp"
            else:
                self.llm = None
        except Exception:
            self.llm = None

        # Si no hay backend local, intentar remoto si está configurado
        if not self.available:
            provider = os.getenv("REMOTE_PROVIDER")
            if provider:
                self.llm = RemoteLLM()
                self.backend = "remote"
                self.available = True

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        # Local llama_cpp
        if self.backend == "llama_cpp" and self.llm is not None:
            try:
                r = self.llm(prompt, max_tokens=max_tokens)
                if isinstance(r, dict) and "choices" in r:
                    return r["choices"][0]["text"].strip()
                return str(r)
            except Exception as e:
                return f"[LLM error] {e}"

        # Remote
        if self.backend == "remote" and self.llm is not None:
            try:
                return self.llm.generate(prompt, max_tokens=max_tokens)
            except Exception as e:
                return f"[Remote error] {e}"

        # Fallback behaviour: respuestas canned
        low = prompt.lower()
        if "hola" in low or "buen" in low:
            return "Hola — soy tu asistente JARVIS local. Dime cómo te puedo ayudar."
        if "abrir" in low and "programa" in low:
            return "Puedo abrir programas con el comando `!open <ruta>` o ejecutar `!exec <comando>`."
        return (
            "Lo siento, no hay un modelo local configurado ni proveedor remoto activo.\n"
            "Para usar un modelo local, descarga un gguf/ggml compatible y pon la ruta en MODEL_PATH en `.env`.\n"
            "Para usar un modelo remoto, configura REMOTE_PROVIDER=hf, REMOTE_MODEL y HF_API_KEY en `.env`."
        )
