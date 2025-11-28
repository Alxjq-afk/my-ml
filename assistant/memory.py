"""Persistencia de memoria simple (JSON file)."""
from pathlib import Path
import json
from datetime import datetime


DATA_DIR = Path("assistant_data")
MEMORY_FILE = DATA_DIR / "memory.json"


def _ensure():
    DATA_DIR.mkdir(exist_ok=True)
    if not MEMORY_FILE.exists():
        MEMORY_FILE.write_text(json.dumps({"memories": []}, indent=2, ensure_ascii=False))


class Memory:
    """Clase para gestionar la memoria de JARVIS."""
    
    def __init__(self):
        """Inicializar memoria."""
        _ensure()
    
    def add(self, role: str, text: str):
        """Agregar entrada a memoria."""
        add_memory(role, text)
    
    def list(self, limit: int = 50):
        """Listar memorias."""
        return list_memories(limit)
    
    def clear(self):
        """Limpiar memoria."""
        clear_memories()


def add_memory(role: str, text: str):
    _ensure()
    data = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "role": role,
        "text": text,
    }
    data["memories"].append(entry)
    MEMORY_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def list_memories(limit: int = 50):
    _ensure()
    data = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    return data.get("memories", [])[-limit:]


def clear_memories():
    _ensure()
    MEMORY_FILE.write_text(json.dumps({"memories": []}, indent=2, ensure_ascii=False), encoding="utf-8")
