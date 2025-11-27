"""Wrapper minimal para un modelo local (scaffold).

Intenta cargar `llama_cpp` si está disponible y `MODEL_PATH` en `.env`.
Si no hay modelo, devuelve respuestas de fallback instructivas.
"""
from typing import Optional
import os


class LocalLLM:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or os.getenv("MODEL_PATH")
        self.backend = None
        self.available = False
        # Try to import llama_cpp (optional)
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

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        if self.available and self.llm is not None:
            try:
                r = self.llm(prompt, max_tokens=max_tokens)
                # llama_cpp returns dict with 'choices'
                if isinstance(r, dict) and "choices" in r:
                    return r["choices"][0]["text"].strip()
                return str(r)
            except Exception as e:
                return f"[LLM error] {e}"

        # Fallback behaviour: simple canned responses / instruction
        low = prompt.lower()
        if "hola" in low or "buen" in low:
            return "Hola — soy tu asistente JARVIS local. Dime cómo te puedo ayudar."
        if "abrir" in low and "programa" in low:
            return "Puedo abrir programas con el comando `!open <ruta>` o ejecutar `!exec <comando>`."
        return (
            "Lo siento, no hay un modelo local configurado.\n"
            "Para usar un modelo local, descarga un modelo ggml compatible (p.ej. GPT4All o Llama ggml) y
coloca la ruta en la variable MODEL_PATH en `.env`."
        )
