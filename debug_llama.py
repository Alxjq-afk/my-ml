import traceback, os
from assistant import config

config.load_config()
model = config.get("MODEL_PATH")
print("MODEL_PATH:", model)
print("Exists:", os.path.exists(model) if model else False)
try:
    from llama_cpp import Llama
    print("llama_cpp imported OK")
    print("Intentando cargar modelo...")
    L = Llama(model_path=model)
    print("Modelo cargado OK")
    resp = L("Eres un asistente. Di 'Hola'", max_tokens=20)
    print("Generación:", resp)
except Exception as e:
    print("Exception raised:")
    traceback.print_exc()
