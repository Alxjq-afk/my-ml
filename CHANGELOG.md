# CHANGELOG

Todas las modificaciones relevantes del proyecto se documentan aquí.

## [v0.1.0] - 2025-11-26
### Añadido
- Esqueleto del proyecto para entrenar modelos de IA (`train.py`).
  - Soporta backend PyTorch (si está instalado) y fallback a scikit-learn (MLPClassifier).
  - Argumentos CLI: `--epochs`, `--batch-size`, `--lr`, `--save-dir`, `--save-every`, `--backend`, `--device`, `--seed`, `--resume`, `--tb`, `--val-size`, `--patience`, `--monitor`.
  - Checkpointing (PyTorch) y guardado final del modelo.
  - Reanudación desde checkpoint (`--resume`).
  - Early stopping y separación train/val/test.
  - Soporte opcional para TensorBoard (`--tb`).
- Inferencia: `predict.py` para cargar checkpoints y hacer predicciones (PyTorch `.pt` y sklearn `.joblib/.pkl`).
- Serialización: uso de `torch.save` para PyTorch y `joblib`/`pickle` para sklearn.
- Tests: suite básica con `pytest` (`tests/test_train.py`) para verificar pipeline mínimo.
- CI: workflow de GitHub Actions en `.github/workflows/ci.yml` que instala dependencias y ejecuta `pytest`.
- Scripts de ayuda: `commit_readme.ps1` (PowerShell) para commitear README cuando `git` esté disponible.
- Documentación: `README.md` actualizado con instrucciones de uso, ejemplos y opciones CLI.
- Release: etiqueta y release `v0.1.0` creada en GitHub.

### Cambiado
- Badge de CI en `README.md` actualizado para apuntar al repositorio remoto actual.

### Notas
- Para reproducibilidad, fijar `--seed` y registrar `pip freeze` si se necesita un entorno exacto.
- Si se desea mover el repositorio a otra cuenta/organización, actualizar los remotos y badges según corresponda.

---

Para futuros cambios: añadir un `CHANGELOG` estructurado por convención [Keep a Changelog](https://keepachangelog.com/) y automatizar releases con GitHub Actions (p. ej. `release-drafter`).
