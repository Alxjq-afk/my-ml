#!/usr/bin/env python3
"""
Script simple de inferencia para los modelos guardados por `train.py`.
Soporta PyTorch (`model_final.pt` o `best_model.pt`) y scikit-learn (`sklearn_mlp.joblib` o `sklearn_mlp.pkl`).

Uso:
    python predict.py --backend auto --model-path checkpoints/best_model.pt

"""
import argparse
import numpy as np
import os


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--backend", choices=["auto", "torch", "sklearn"], default="auto")
    p.add_argument("--model-path", type=str, required=True)
    return p.parse_args()


def main():
    args = parse_args()
    path = args.model_path
    if not os.path.exists(path):
        print(f"Modelo no encontrado: {path}")
        return

    backend = args.backend
    if backend == "auto":
        # inferir por extensión
        ext = os.path.splitext(path)[1].lower()
        if ext in [".pt"]:
            backend = "torch"
        elif ext in [".joblib", ".pkl"]:
            backend = "sklearn"

    if backend == "torch":
        try:
            import torch
            import torch.nn as nn
        except Exception:
            print("PyTorch no disponible en este entorno.")
            return

        # Para este ejemplo asumimos la misma arquitectura Net usada en train.py
        from train import Net
        device = torch.device("cpu")
        model = Net()
        state = torch.load(path, map_location=device)
        # soportar checkpoint con dict o state_dict plano
        if isinstance(state, dict) and "model_state_dict" in state:
            model.load_state_dict(state["model_state_dict"])
        else:
            model.load_state_dict(state)
        model.eval()

        # inferir sobre una muestra aleatoria del dataset digits
        from sklearn.datasets import load_digits
        X, y = load_digits(return_X_y=True)
        X = X.astype("float32") / 16.0
        sample = torch.from_numpy(X[:5])
        with torch.no_grad():
            logits = model(sample)
            preds = logits.argmax(dim=1).numpy()
        print("Predicciones (PyTorch):", preds)

    else:
        # sklearn
        try:
            import joblib
        except Exception:
            joblib = None

        if joblib is not None and path.endswith(".joblib"):
            m = joblib.load(path)
            scaler = None
            # intentar cargar scaler en mismo directorio
            scpath = os.path.join(os.path.dirname(path), "scaler.joblib")
            if os.path.exists(scpath):
                scaler = joblib.load(scpath)
            from sklearn.datasets import load_digits
            X, y = load_digits(return_X_y=True)
            Xs = scaler.transform(X[:5]) if scaler is not None else X[:5]
            preds = m.predict(Xs)
            print("Predicciones (sklearn):", preds)
        else:
            # intentar cargar pickle
            import pickle
            with open(path, "rb") as f:
                data = pickle.load(f)
            model = data.get("model") if isinstance(data, dict) else data
            scaler = data.get("scaler") if isinstance(data, dict) else None
            from sklearn.datasets import load_digits
            X, y = load_digits(return_X_y=True)
            Xs = scaler.transform(X[:5]) if scaler is not None else X[:5]
            preds = model.predict(Xs)
            print("Predicciones (sklearn pickle):", preds)


if __name__ == "__main__":
    main()
