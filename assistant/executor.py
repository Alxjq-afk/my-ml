"""Ejecutor de acciones: ejecutar comandos, abrir archivos, controlar volumen y enviar correo."""
import subprocess
import os
import sys
from pathlib import Path
import smtplib
from email.message import EmailMessage

try:
    # pycaw para control de volumen en Windows
    from ctypes import POINTER, cast
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    _HAS_PYCAW = True
except Exception:
    _HAS_PYCAW = False


def execute_command(cmd: str) -> dict:
    """Ejecuta un comando shell y devuelve salida y código."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return {"returncode": res.returncode, "stdout": res.stdout, "stderr": res.stderr}
    except Exception as e:
        return {"returncode": -1, "stdout": "", "stderr": str(e)}


def open_path(path: str) -> bool:
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform.startswith("darwin"):
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        return True
    except Exception:
        return False


def set_volume(percent: int) -> bool:
    if not _HAS_PYCAW:
        return False
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        # percent 0-100 to volume range
        vol_range = volume.GetVolumeRange()
        minv, maxv = vol_range[0], vol_range[1]
        val = minv + (maxv - minv) * (percent / 100.0)
        volume.SetMasterVolumeLevel(val, None)
        return True
    except Exception:
        return False


def send_email(smtp_host: str, smtp_port: int, username: str, password: str, to: str, subject: str, body: str) -> bool:
    try:
        msg = EmailMessage()
        msg["From"] = username
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
        return True
    except Exception:
        return False
