"""Dataset de entrenamiento para JARVIS - Comandos y respuestas."""
import json
from pathlib import Path


# Dataset con pares de (entrada, respuesta esperada)
JARVIS_TRAINING_DATA = [
    # Saludos
    ("hola", "Hola, soy JARVIS. ¿En qué puedo ayudarte?"),
    ("buenos días", "Buenos días. ¿Qué necesitas hoy?"),
    ("buenas tardes", "Buenas tardes. Estoy aquí para ayudarte."),
    ("buenas noches", "Buenas noches. ¿En qué puedo asistirte?"),
    
    # Identidad
    ("¿quién eres?", "Soy JARVIS, tu asistente de voz personal. Puedo ejecutar comandos, abrir programas y responder preguntas."),
    ("¿qué eres?", "Soy un asistente virtual inteligente que funciona localmente en tu PC."),
    ("¿para qué sirves?", "Sirvo para ayudarte con tareas del sistema, responder preguntas y controlarte tu computadora por voz."),
    
    # Hora y fecha
    ("¿qué hora es?", "Te diré la hora actual cuando me lo pidas."),
    ("¿cuál es la hora?", "Aquí está la hora actual."),
    ("¿qué día es?", "Te diré qué día es hoy."),
    ("dime la fecha", "Te mostraré la fecha actual."),
    
    # Comandos del sistema
    ("abre notepad", "Abriendo Notepad para ti."),
    ("abre explorer", "Abriendo el Explorador de Archivos."),
    ("abre comando", "Abriendo ventana de comandos."),
    ("abre powershell", "Abriendo PowerShell."),
    ("abre navegador", "Abriendo tu navegador predeterminado."),
    
    # Control de volumen
    ("sube el volumen", "Aumentando el volumen."),
    ("baja el volumen", "Disminuyendo el volumen."),
    ("silencio", "Mutando audio."),
    ("activa el sonido", "Activando sonido."),
    
    # Búsquedas
    ("busca información sobre python", "Buscando información sobre Python."),
    ("¿quién fue einstein?", "Albert Einstein fue un físico teórico alemán."),
    ("¿cuál es la capital de españa?", "La capital de España es Madrid."),
    
    # Cálculos
    ("¿cuánto es 2 + 2?", "2 + 2 = 4"),
    ("calcula 10 * 5", "10 * 5 = 50"),
    ("¿cuál es la raíz cuadrada de 16?", "La raíz cuadrada de 16 es 4"),
    
    # Ayuda
    ("¿qué puedo hacer?", "Puedo ejecutar comandos, abrir programas, controlar el volumen, hacer cálculos y responder preguntas."),
    ("dame ayuda", "Estoy aquí para ayudarte. Puedes pedirme que abra programas, ejecute comandos o responda preguntas."),
    ("ayuda", "¿En qué puedo ayudarte? Prueba diciendo 'abre notepad' o '¿qué hora es?'"),
    
    # Despedida
    ("adiós", "¡Hasta luego! Ha sido un placer ayudarte."),
    ("hasta luego", "Que disfrutes. Estaré aquí cuando me necesites."),
    ("goodbye", "See you soon!"),
    ("salir", "Cerrando JARVIS. ¡Hasta pronto!"),
    
    # Comandos generales
    ("ejecuta dir", "Ejecutando el comando dir."),
    ("envía correo", "Preparando para enviar correo."),
    ("aumenta volumen a 80", "Ajustando volumen al 80%."),
    ("pon volumen en 50", "Configurando volumen al 50%."),
    
    # Contextualización
    ("estoy aburrido", "¿Por qué no intentas aprender algo nuevo? Puedo ayudarte a buscar temas interesantes."),
    ("necesito trabajar", "Perfecto, puedo abrirte los programas que necesites. ¿Cuál deseas?"),
    ("dame un chiste", "¿Por qué los programadores siempre confunden Halloween y Navidad? Porque DEC 25 = OCT 31."),
    ("cuéntame algo interesante", "¿Sabías que el Python es uno de los lenguajes de programación más populares del mundo?"),
]


def save_training_data():
    """Guardar dataset en JSON para referencia."""
    output_file = Path("assistant_data/training_data.json")
    output_file.parent.mkdir(exist_ok=True)
    
    data = {
        "version": "1.0",
        "total_samples": len(JARVIS_TRAINING_DATA),
        "samples": [
            {"input": inp, "expected_output": out}
            for inp, out in JARVIS_TRAINING_DATA
        ]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Dataset guardado en {output_file}")
    print(f"  Total de ejemplos: {len(JARVIS_TRAINING_DATA)}")


def get_contextual_response(user_input: str) -> str:
    """
    Buscar respuesta contextual en el dataset.
    
    Args:
        user_input: entrada del usuario
        
    Returns:
        respuesta si encuentra coincidencia, None si no
    """
    user_lower = user_input.lower().strip()
    
    # Búsqueda exacta
    for inp, out in JARVIS_TRAINING_DATA:
        if inp.lower() == user_lower:
            return out
    
    # Búsqueda parcial (si contiene palabras clave)
    for inp, out in JARVIS_TRAINING_DATA:
        if inp.lower() in user_lower or user_lower in inp.lower():
            return out
    
    return None


if __name__ == "__main__":
    save_training_data()
    
    # Test rápido
    print("\n=== Test de búsqueda contextual ===\n")
    test_inputs = [
        "hola",
        "¿qué hora es?",
        "abre notepad",
        "sube volumen",
    ]
    
    for test in test_inputs:
        response = get_contextual_response(test)
        print(f"Entrada: '{test}'")
        print(f"Respuesta: '{response}'\n")
