#!/usr/bin/env python3
"""Runner para el asistente JARVIS (CLI)."""
import argparse
import sys
import threading
from assistant import config, llm, memory, executor, voice


def main():
    parser = argparse.ArgumentParser(prog="jarvis")
    parser.add_argument("--confirm-actions", action="store_true", help="Pedir confirmación antes de ejecutar acciones")
    args = parser.parse_args()

    config.load_config()
    model_path = config.get("MODEL_PATH")
    L = llm.LocalLLM(model_path=model_path)

    print("JARVIS (MVP) - CLI (escribe 'exit' para salir)")
    if model_path:
        print(f"Intentando usar modelo local: {model_path}")
    else:
        print("No hay modelo local configurado. Usa un modelo o sigue con el fallback.")

    while True:
        try:
            txt = input("Tú> ")
        except (KeyboardInterrupt, EOFError):
            print("\nSaliendo...")
            sys.exit(0)

        if not txt:
            continue
        if txt.strip().lower() in ("exit", "quit", "salir"):
            print("Adiós.")
            break

        # comandos especiales
        if txt.startswith("!exec "):
            cmd = txt[len("!exec "):]
            if args.confirm_actions:
                c = input(f"Confirmar ejecutar: {cmd} (y/n): ")
                if c.lower() != "y":
                    print("Cancelado")
                    continue
            out = executor.execute_command(cmd)
            print(out.get("stdout") or out.get("stderr") or out)
            memory.add_memory("assistant", f"Ejecutado: {cmd}")
            continue

        if txt.startswith("!open "):
            path = txt[len("!open "):]
            ok = executor.open_path(path)
            print("Abierto" if ok else "No se pudo abrir")
            memory.add_memory("assistant", f"Abierto: {path}")
            continue

        if txt.startswith("!vol "):
            parts = txt.split()
            if len(parts) >= 2:
                action = parts[1]
                if action in ("up", "down") and len(parts) == 3:
                    try:
                        val = int(parts[2])
                        executor.set_volume(val)
                        print(f"Volumen ajustado a {val}")
                    except Exception:
                        print("Valor inválido")
                elif action == "set" and len(parts) == 3:
                    try:
                        val = int(parts[2])
                        executor.set_volume(val)
                        print(f"Volumen fijado a {val}")
                    except Exception:
                        print("Valor inválido")
                else:
                    print("Uso: !vol set <0-100>")
            continue

        if txt.startswith("!sendmail"):
            # flujo simple: pedimos datos mínimos
            smtp = config.get("SMTP_HOST")
            port = int(config.get("SMTP_PORT", 587))
            user = config.get("SMTP_USER")
            pwd = config.get("SMTP_PASS")
            to = input("Para: ")
            subject = input("Asunto: ")
            body = input("Cuerpo: ")
            ok = executor.send_email(smtp, port, user, pwd, to, subject, body)
            print("Enviado" if ok else "Fallo al enviar")
            memory.add_memory("assistant", f"Enviado email a {to} asunto {subject}")
            continue

        # normal: enviar al LLM
        prompt = f"Eres JARVIS en español. Responde de forma cortés y proactiva. Usuario: {txt}"
        resp = L.generate(prompt)
        print("JARVIS>", resp)
        # TTS: hablar la respuesta en hilo para no bloquear
        try:
            t = threading.Thread(target=voice.speak, args=(resp,))
            t.daemon = True
            t.start()
        except Exception:
            pass
        memory.add_memory("user", txt)
        memory.add_memory("assistant", resp)


if __name__ == "__main__":
    main()
