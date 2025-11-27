#!/usr/bin/env python3
"""Test del intérprete de comandos naturales."""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from assistant.interpreter import CommandInterpreter

CI = CommandInterpreter()

print('=== TEST: Intérprete de Comandos Naturales ===\n')

test_commands = [
    'abre notepad',
    'ejecuta dir',
    'sube el volumen a 70',
    'baja volumen',
    'envía un correo',
    'abre explorer',
    'lanza powershell',
    'pon volumen a 50',
    'hola, cómo estás',
]

for cmd in test_commands:
    result = CI.interpret(cmd)
    print(f'Entrada: "{cmd}"')
    print(f'Tipo: {result["type"]}')
    print(f'Mensaje: {result["message"]}')
    if result['type'] == 'exec':
        print(f'  → Comando: {result["command"]}')
    elif result['type'] == 'open':
        print(f'  → Programa: {result["path"]}')
    elif result['type'] == 'volume':
        print(f'  → Acción: {result["action"]}, Valor: {result["value"]}')
    print()
