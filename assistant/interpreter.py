r"""Interprete de comandos naturales para JARVIS.

Convierte instrucciones en lenguaje natural a comandos del sistema.
Ejemplos:
  - abre notepad -> open C:\Windows\Notepad.exe
  - ejecuta dir -> exec dir
  - sube el volumen -> vol set 70
  - envia un correo -> sendmail
"""

import re
import os
from pathlib import Path


class CommandInterpreter:
    """Interpreta comandos naturales en español y los traduce a acciones."""

    # Mapeo de programas comunes (nombre -> ruta en Windows)
    COMMON_PROGRAMS = {
        "notepad": "C:\\Windows\\Notepad.exe",
        "bloc de notas": "C:\\Windows\\Notepad.exe",
        "block de notas": "C:\\Windows\\Notepad.exe",
        "explorer": "C:\\Windows\\explorer.exe",
        "explorador": "C:\\Windows\\explorer.exe",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "powershell": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        "cmd": "C:\\Windows\\System32\\cmd.exe",
        "consola": "C:\\Windows\\System32\\cmd.exe",
        "terminal": "C:\\Windows\\System32\\cmd.exe",
        "paint": "C:\\Windows\\System32\\mspaint.exe",
        "pintura": "C:\\Windows\\System32\\mspaint.exe",
        "calculadora": "C:\\Windows\\System32\\calc.exe",
        "calculator": "C:\\Windows\\System32\\calc.exe",
        "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    }

    def __init__(self):
        pass

    def interpret(self, text: str) -> dict:
        """
        Interpreta un comando natural y devuelve tipo de comando + parámetros.

        Returns:
            {
                "type": "exec" | "open" | "volume" | "sendmail" | "conversation",
                "command": "...",  # Para exec
                "path": "...",     # Para open
                "action": "up"|"down"|"set",  # Para volume
                "value": 50,       # Para volume set
                "success": True|False,
                "message": "..."
            }
        """
        low = text.lower().strip()

        # 1. Detectar comando EXEC (ejecutar comando)
        exec_patterns = [
            r"^(?:ejecuta?|corre?|run)\s+(.+)$",
            r"^(?:lanza?|inicia?)\s+(?:comando|cmd)?\s*(.+)$",
            r"^haz\s+(?:ejecutar|correr|run)\s+(.+)$",
        ]
        for pattern in exec_patterns:
            match = re.match(pattern, low)
            if match:
                command = match.group(1).strip()
                return {
                    "type": "exec",
                    "command": command,
                    "success": True,
                    "message": f"Ejecutando: {command}",
                }

        # 2. Detectar comando OPEN (abrir archivo/programa)
        open_patterns = [
            r"^(?:abre?|open|lanza?|inicia?)\s+(\w+)\b",
            r"^(?:abre?|open)\s+(?:el\s+)?(?:programa|app|archivo)?\s*(.+)$",
            r"^haz\s+(?:que\s+)?(?:abra?|open)\s+(.+)$",
        ]
        for pattern in open_patterns:
            match = re.match(pattern, low)
            if match:
                program_name = match.group(1).strip()
                path = self._resolve_program(program_name)
                if path and os.path.exists(path):
                    return {
                        "type": "open",
                        "path": path,
                        "success": True,
                        "message": f"Abriendo: {program_name}",
                    }
                else:
                    return {
                        "type": "open",
                        "path": program_name,  # Intentar abierto como ruta
                        "success": True,
                        "message": f"Abriendo: {program_name}",
                    }

        # 3. Detectar comando VOLUME (controlar volumen)
        volume_patterns = [
            (r"(?:sube?|aumenta?|incrementa?)\s+(?:el\s+)?volumen\s+(?:a\s+)?(\d+)?", "set", "up"),
            (r"(?:baja?|disminuye?|reduce?)\s+(?:el\s+)?volumen\s+(?:a\s+)?(\d+)?", "set", "down"),
            (r"(?:pon|fija?)\s+(?:el\s+)?volumen\s+(?:a\s+)?(\d+)", "set", None),
            (r"volumen\s+(?:a\s+)?(\d+)", "set", None),
            (r"sube?.*volumen", None, "up"),
            (r"baja?.*volumen", None, "down"),
        ]
        for pattern, default_action, fallback_action in volume_patterns:
            match = re.search(pattern, low)
            if match:
                action = default_action or fallback_action or "set"
                value = 50  # Default
                if match.groups() and match.group(1):
                    try:
                        value = int(match.group(1))
                        value = max(0, min(100, value))  # Clamp 0-100
                    except ValueError:
                        pass

                return {
                    "type": "volume",
                    "action": action,
                    "value": value,
                    "success": True,
                    "message": f"Ajustando volumen a {value}",
                }

        # 4. Detectar comando SENDMAIL (enviar correo)
        sendmail_patterns = [
            r"(?:envía?|manda?)\s+(?:un\s+)?correo",
            r"(?:envía?|manda?)\s+(?:un\s+)?email",
            r"(?:envía?|manda?)\s+(?:un\s+)?mail",
            r"(?:quiero\s+)?enviar\s+correo",
        ]
        for pattern in sendmail_patterns:
            if re.search(pattern, low):
                return {
                    "type": "sendmail",
                    "success": True,
                    "message": "Preparando envío de correo...",
                }

        # 5. Si no detectó nada, es conversación normal
        return {
            "type": "conversation",
            "success": True,
            "message": None,
        }

    def _resolve_program(self, program_name: str) -> str:
        """Resuelve un nombre de programa a su ruta real."""
        low = program_name.lower().strip()

        # Buscar en mapeo conocido
        if low in self.COMMON_PROGRAMS:
            return self.COMMON_PROGRAMS[low]

        # Buscar coincidencias parciales
        for name, path in self.COMMON_PROGRAMS.items():
            if name.startswith(low) or low.startswith(name):
                return path

        # Si no está en el mapeo, devolver como está (podría ser una ruta)
        return program_name
