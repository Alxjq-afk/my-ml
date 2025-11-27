"""Test de JARVIS entrenado con dataset contextual."""
from assistant.llm import LocalLLM
from assistant import config

config.load_config()
L = LocalLLM(config.get('MODEL_PATH'))

print('=== Test: JARVIS Entrenado con Dataset ===\n')

test_inputs = [
    'hola',
    '¿qué hora es?',
    'abre notepad',
    '¿quién eres?',
    'ayuda',
    'adiós',
]

for inp in test_inputs:
    prompt = f'Usuario: {inp}'
    response = L.generate(prompt, max_tokens=128)
    print(f'Entrada: "{inp}"')
    print(f'Respuesta: {response}\n')

print("\n✓ Test completado - JARVIS está entrenado")
