[![CI](https://github.com/Alxjq-afk/my-ml/actions/workflows/ci.yml/badge.svg)](https://github.com/Alxjq-afk/my-ml/actions/workflows/ci.yml)

# ML + JARVIS Assistant

Proyecto integrado con dos componentes principales:

## 📊 1. Machine Learning (train.py / predict.py)

Entrenamiento e inferencia de modelos de IA.

## 🤖 2. JARVIS Assistant (Advanced Voice v2.0)

Asistente de voz tipo Cortana/Alexa con:
- **Escucha continua** con detección de palabra clave ("Hey JARVIS")
- **Speech-to-Text** con Whisper (OpenAI)
- **Modelos de lenguaje**: Mistral 7B local + Hugging Face remoto
- **Comandos naturales**: "abre notepad", "sube volumen", etc.
- **APIs integradas**: hora, clima, búsqueda web, info del sistema
- **Text-to-Speech**: respuestas de voz

**Documentación completa**: Ver [`JARVIS_ADVANCED.md`](JARVIS_ADVANCED.md)

---

## 🚀 Quick Start

### JARVIS (Voice Assistant)
```bash
# Modo texto (CLI)
python run_jarvis_voice.py --mode cli

# Modo voz (escucha continua)
python run_jarvis_voice.py --mode voice

# Modo híbrido (auto-detecta)
python run_jarvis_voice.py
```

**Ejemplo de comandos**:
```
"abre notepad"          → Abre Notepad
"ejecuta dir C:\"       → Ejecuta comando
"sube volumen a 70"     → Ajusta volumen
"¿Qué hora es?"         → Pregunta a JARVIS
```

### ML Training
```bash
python train.py --epochs 20 --batch-size 32
python predict.py --model model_final.pt --input test_data.csv
```

---

## 📦 Contenido del proyecto:
- `train.py`: script de entrenamiento que utiliza PyTorch si está instalado; si no, usa scikit-learn (MLP) como fallback. Dataset por defecto: `digits` de scikit-learn (pequeño y sin descargas).
- `requirements.txt`: dependencias mínimas.
- `predict.py`: script de inferencia para modelos guardados (PyTorch `.pt` o sklearn `.joblib/.pkl`).
- `.github/workflows/ci.yml`: workflow de CI que ejecuta los tests con `pytest`.

Cómo usar (PowerShell):

1) Crear/activar tu entorno virtual (opcional pero recomendado):

    python -m venv .venv; .\.venv\Scripts\Activate.ps1

2) Instalar dependencias mínimas:

    pip install -r requirements.txt

Si quieres usar PyTorch (opcional): visita https://pytorch.org/get-started/locally/ para instalar la versión adecuada para tu sistema.

3) Ejecutar el script:

    python train.py

Notas:
- Si PyTorch está instalado, el script entrenará una pequeña red en PyTorch (CPU/GPU si está disponible).
- Si PyTorch no está instalado, el script entrenará un `MLPClassifier` de scikit-learn sobre el dataset `digits`.

Características incluidas en esta versión:
- Guardado de checkpoints y modelos (PyTorch: `checkpoint_epoch{N}.pt`, `model_final.pt`; sklearn: `sklearn_mlp.joblib` / `sklearn_mlp.pkl`).
- Reanudación desde checkpoint (`--resume`) para PyTorch.
- Early stopping y separación train/val/test (`--val-size`, `--patience`, `--monitor`).
- Soporte opcional de TensorBoard (`--tb`) para registrar métricas.
- `predict.py` para hacer inferencia con los modelos guardados.
- Tests unitarios con `pytest` y workflow de CI (`.github/workflows/ci.yml`).

Siguientes pasos recomendados (opcionales):
- Sustituir `load_digits` por un dataset propio o por `torchvision.datasets` para datasets más grandes.
- Integrar Weights & Biases (W&B) u otro sistema de tracking para experimentos.

Detalles y ejemplos de uso
-------------------------

El script ahora acepta varios argumentos desde la línea de comandos (usa `python train.py --help` para verlos todos):

- `--epochs` (int): número de épocas (por defecto 10)
- `--batch-size` (int): tamaño de batch (por defecto 64)
- `--lr` (float): learning rate (por defecto 1e-3)
- `--save-dir` (str): directorio donde guardar checkpoints y modelos
- `--save-every` (int): cada N épocas guardar checkpoint (PyTorch)
- `--backend` (auto|torch|sklearn): forzar backend (por defecto `auto`)
- `--device` (auto|cpu|cuda): forzar dispositivo (solo PyTorch)
- `--seed` (int): semilla para reproducibilidad (random, numpy, torch)
- `--resume` (str): ruta a checkpoint PyTorch para reanudar entrenamiento

Flags nuevos para validación y early stopping
-------------------------------------------

- `--val-size` (float): fracción del dataset usada para validación (por defecto 0.1). El dataset se divide en train/val/test.
- `--patience` (int): paciencia para early stopping (número de epochs sin mejora antes de detenerse). Por defecto 3.
- `--monitor` (accuracy|loss): métrica a monitorizar para decidir mejoras y guardar el mejor modelo. Por defecto `accuracy`.

Ejemplos con early stopping y validación
---------------------------------------

- Entrenar con validación y early stopping (PyTorch):

    python train.py --epochs 50 --val-size 0.15 --patience 5 --save-dir checkpoints_es

- Forzar backend scikit-learn con early stopping y TensorBoard logging:

    python train.py --backend sklearn --val-size 0.15 --patience 5 --tb --save-dir checkpoints_skes

Notas sobre early stopping
-------------------------

- El script ahora separa el dataset en train/val/test. La validación se usa para monitorizar la métrica indicada en `--monitor`.
- Si no hay mejora durante `--patience` epochs, el entrenamiento se detiene y el mejor checkpoint (según la métrica) queda en `--save-dir`.


Ejemplos prácticos (PowerShell):

- Entrenar 20 épocas en el backend detectado (PyTorch si está instalado):

    python train.py --epochs 20 --batch-size 64 --lr 0.001

- Guardar checkpoints en `checkpoints` cada 2 épocas:

    python train.py --save-dir checkpoints --save-every 2 --epochs 10

- Forzar uso de CPU y fijar semilla para reproducibilidad:

    python train.py --device cpu --seed 42 --save-dir checkpoints

- Reanudar desde un checkpoint guardado (PyTorch):

    python train.py --resume checkpoints\checkpoint_epoch3.pt --save-dir checkpoints --epochs 10

- Forzar backend scikit-learn (usa joblib/pickle para guardar el modelo):

    python train.py --backend sklearn --save-dir checkpoints_sklearn

Notas sobre `--resume` y guardado
--------------------------------

- Cuando usas `--resume` con un checkpoint generado por PyTorch, el script intentará cargar el estado del modelo y también el estado del optimizador (si está presente). Si el estado del optimizador no es compatible por diferencias de versión, el script continuará desde el modelo cargado pero podría no restaurar exactamente el optimizador.
- Los checkpoints de PyTorch se guardan como `checkpoint_epoch{N}.pt` y el modelo final como `model_final.pt` en `--save-dir`.
- El backend sklearn guarda `sklearn_mlp.joblib` y `scaler.joblib` (si `joblib` está disponible). Si joblib no funciona, se guarda un `sklearn_mlp.pkl` con pickle como fallback.

Recomendaciones rápidas
---------------------

- Si tienes GPU y quieres usarla, instala PyTorch con soporte CUDA desde la web oficial; el script usará automáticamente `cuda` si está disponible a menos que pases `--device cpu`.
- Para experimentos reproducibles, fija `--seed` y anota la versión de las librerías (p. ej. `pip freeze > requirements-freeze.txt`).
- Si quieres monitorización, puedo añadir TensorBoard o integración con Weights & Biases en el siguiente paso.

Si quieres que añada integración con Weights & Biases, más tests (p. ej. cobertura para PyTorch), ejemplos de configuración (`yaml`) o pipelines de deployment, dime qué prefieres y lo implemento.

Integración continua (CI)
-------------------------

Este repositorio incluye un workflow de GitHub Actions en `.github/workflows/ci.yml` que instala las dependencias desde `requirements.txt` y ejecuta la suite de tests (`pytest`). Cada push y pull request contra `main`/`master` activará el CI.

