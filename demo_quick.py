"""Demo rápida de intérprete de comandos."""
from assistant.interpreter import CommandInterpreter

CI = CommandInterpreter()
commands = [
    'abre notepad',
    'ejecuta dir',
    'sube volumen a 80',
    'envía correo',
    'hola cómo estás'
]

print('=== Demo Rápida: Comandos Naturales ===\n')
for cmd in commands:
    result = CI.interpret(cmd)
    print(f'Entrada: "{cmd}"')
    print(f'Tipo: {result["type"]}')
    print(f'Mensaje: {result["message"]}')
    print()
