#!/usr/bin/env python3
"""
Script base de entrenamiento.
- Si está disponible, usa PyTorch para entrenar una red simple sobre el dataset "digits" de scikit-learn.
- Si PyTorch no está instalado, usa scikit-learn (MLPClassifier) como fallback.

Uso:
    python train.py

Notas:
- Instala dependencias con: pip install -r requirements.txt
- PyTorch es opcional; si está instalado se usará automáticamente.
"""

import sys
import numpy as np
import argparse
import os
import random
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Intentar usar PyTorch; si falla, usaremos scikit-learn
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import TensorDataset, DataLoader
    USE_TORCH = True
except Exception:
    USE_TORCH = False


def load_data(test_size=0.2, val_size=0.1, random_state=42):
    """Carga el dataset y devuelve splits: X_train, X_val, X_test, y_train, y_val, y_test.
    val_size es la fracción del total dedicada a validación; test_size es fracción para test.
    """
    X, y = load_digits(return_X_y=True)
    X = X.astype("float32") / 16.0  # los píxeles van de 0..16
    # Primero separar test
    X_rest, X_test, y_rest, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    # Ahora separar validación desde el resto
    if val_size > 0:
        # val fraction relative to the rest
        rel_val = val_size / (1.0 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(X_rest, y_rest, test_size=rel_val, random_state=random_state, stratify=y_rest)
    else:
        X_train, X_val, y_train, y_val = X_rest, None, y_rest, None

    return X_train, X_val, X_test, y_train, y_val, y_test


if USE_TORCH:
    class Net(nn.Module):
        def __init__(self, input_dim=64, hidden=128, num_classes=10):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(input_dim, hidden),
                nn.ReLU(),
                nn.Linear(hidden, num_classes)
            )

        def forward(self, x):
            return self.net(x)


    def train_torch(X_train, X_val, X_test, y_train, y_val, y_test, epochs=10, batch_size=64, lr=1e-3, save_dir=None, save_every=1, device=None, resume_path=None, tb_writer=None, patience=3, monitor="accuracy"):
        # device: torch.device or None (auto)
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Usando PyTorch en: {device}")

        X_train_t = torch.from_numpy(X_train)
        y_train_t = torch.from_numpy(y_train).long()
        X_test_t = torch.from_numpy(X_test)
        y_test_t = torch.from_numpy(y_test).long()

        train_ds = TensorDataset(X_train_t, y_train_t)
        train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True)

        # tensores de validación y test
        X_val_t = torch.from_numpy(X_val) if X_val is not None else None
        y_val_t = torch.from_numpy(y_val).long() if y_val is not None else None
        X_test_t = torch.from_numpy(X_test)
        y_test_t = torch.from_numpy(y_test).long()

        model = Net().to(device)
        loss_fn = nn.CrossEntropyLoss()
        opt = optim.Adam(model.parameters(), lr=lr)

        # Crear directorio de guardado si se especifica
        if save_dir:
            os.makedirs(save_dir, exist_ok=True)

        # Si se pide reanudar desde checkpoint
        start_epoch = 1
        if resume_path:
            if os.path.exists(resume_path):
                ckpt = torch.load(resume_path, map_location=device)
                if "model_state_dict" in ckpt:
                    model.load_state_dict(ckpt.get("model_state_dict", {}))
                if "optimizer_state_dict" in ckpt:
                    try:
                        opt.load_state_dict(ckpt["optimizer_state_dict"])
                    except Exception:
                        print("Advertencia: no se pudo cargar el estado del optimizador del checkpoint.")
                start_epoch = ckpt.get("epoch", 0) + 1
                print(f"Reanudando desde checkpoint {resume_path}, comenzando en epoch {start_epoch}")
            else:
                print(f"Resume path {resume_path} no encontrado, empezando desde cero.")

        best_value = None
        if monitor == "accuracy":
            best_value = -1.0
        else:
            best_value = float("inf")
        no_improve = 0
        for epoch in range(start_epoch, epochs + 1):
            model.train()
            running_loss = 0.0
            for xb, yb in train_dl:
                xb = xb.to(device)
                yb = yb.to(device)
                opt.zero_grad()
                out = model(xb)
                loss = loss_fn(out, yb)
                loss.backward()
                opt.step()
                running_loss += loss.item() * xb.size(0)

            avg_loss = running_loss / len(train_dl.dataset)

            # evaluar
            model.eval()
            with torch.no_grad():
                logits = model(X_val_t.to(device))
                preds = logits.argmax(dim=1).cpu().numpy()
                acc = (preds == y_val).mean()

            print(f"Epoch {epoch}/{epochs} - loss: {avg_loss:.4f} - val_acc: {acc:.4f}")

            # TensorBoard: escribir métricas si se proporcionó un writer
            if tb_writer is not None:
                try:
                    tb_writer.add_scalar("train/loss", float(avg_loss), epoch)
                    tb_writer.add_scalar("val/accuracy", float(acc), epoch)
                except Exception:
                    pass

            # Guardar checkpoint cada `save_every` epocas (si se indica save_dir)
            if save_dir and (save_every > 0) and (epoch % save_every == 0):
                ckpt_path = os.path.join(save_dir, f"checkpoint_epoch{epoch}.pt")
                torch.save({
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": opt.state_dict(),
                }, ckpt_path)
                print(f"Checkpoint guardado en: {ckpt_path}")

            # Comprobar mejora según monitor y guardar
            current_value = acc if monitor == "accuracy" else avg_loss
            improved = (current_value > best_value) if monitor == "accuracy" else (current_value < best_value)
            if improved:
                best_value = current_value
                no_improve = 0
                if save_dir:
                    best_path = os.path.join(save_dir, "best_model.pt")
                    torch.save({"epoch": epoch, "model_state_dict": model.state_dict(), monitor: float(current_value)}, best_path)
                    print(f"Mejor modelo guardado en: {best_path} ({monitor}={float(current_value):.4f})")
            else:
                no_improve += 1

            # Early stopping
            if no_improve >= patience:
                print(f"No hay mejora en {patience} epochs; terminando por early stopping.")
                break

        # Guardar modelo final
        if save_dir:
            final_path = os.path.join(save_dir, "model_final.pt")
            torch.save(model.state_dict(), final_path)
            print(f"Modelo final guardado en: {final_path}")


from sklearn.neural_network import MLPClassifier


def train_sklearn(X_train, X_val, X_test, y_train, y_val, y_test, save_dir=None, patience=3, monitor="accuracy", tb_writer=None):
    scaler = StandardScaler()

    X_train_s = scaler.fit_transform(X_train)
    X_val_s = scaler.transform(X_val) if X_val is not None else None
    X_test_s = scaler.transform(X_test)

    # Usaremos warm_start para simular epochs
    clf = MLPClassifier(hidden_layer_sizes=(128,), max_iter=1, warm_start=True, random_state=42)

    best_value = -1.0 if monitor == "accuracy" else float("inf")
    no_improve = 0

    for epoch in range(1, 51):  # límite razonable de epochs para sklearn
        clf.fit(X_train_s, y_train)

        # evaluar en validación
        if X_val_s is not None:
            if monitor == "accuracy":
                val_metric = clf.score(X_val_s, y_val)
            else:
                # calcular loss aproximado (log loss) no trivial; usar 1-accuracy como proxy
                val_metric = 1.0 - clf.score(X_val_s, y_val)
        else:
            val_metric = clf.score(X_test_s, y_test)

        print(f"sklearn Epoch {epoch} - val_{monitor}: {val_metric:.4f}")

        # TensorBoard
        if tb_writer is not None:
            try:
                tb_writer.add_scalar("val/" + monitor, float(val_metric), epoch)
            except Exception:
                pass

        # comprobar mejora
        improved = (val_metric > best_value) if monitor == "accuracy" else (val_metric < best_value)
        if improved:
            best_value = val_metric
            no_improve = 0
            # guardar
            if save_dir:
                os.makedirs(save_dir, exist_ok=True)
                try:
                    import joblib
                    joblib.dump(clf, os.path.join(save_dir, "sklearn_mlp.joblib"))
                    joblib.dump(scaler, os.path.join(save_dir, "scaler.joblib"))
                    print(f"Modelo sklearn guardado en: {os.path.join(save_dir, 'sklearn_mlp.joblib')}")
                except Exception:
                    import pickle
                    with open(os.path.join(save_dir, "sklearn_mlp.pkl"), "wb") as f:
                        pickle.dump({"model": clf, "scaler": scaler}, f)
                    print(f"Modelo sklearn guardado (pickle) en: {os.path.join(save_dir, 'sklearn_mlp.pkl')}")
        else:
            no_improve += 1

        if no_improve >= patience:
            print(f"No hay mejora en {patience} epochs; terminando por early stopping (sklearn).")
            break

    # guardar modelo final si no se guardó
    if save_dir:
        final_path = os.path.join(save_dir, "sklearn_final.joblib")
        try:
            import joblib
            joblib.dump(clf, final_path)
            print(f"Modelo final sklearn guardado en: {final_path}")
        except Exception:
            import pickle
            with open(os.path.join(save_dir, "sklearn_final.pkl"), "wb") as f:
                pickle.dump({"model": clf, "scaler": scaler}, f)
            print(f"Modelo final sklearn guardado (pickle) en: {os.path.join(save_dir, 'sklearn_final.pkl')}")


def parse_args():
    p = argparse.ArgumentParser(description="Entrenamiento base: PyTorch o scikit-learn (fallback).")
    p.add_argument("--epochs", type=int, default=10)
    p.add_argument("--batch-size", type=int, default=64)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--save-dir", type=str, default=None, help="Directorio donde guardar checkpoints/modelos")
    p.add_argument("--save-every", type=int, default=1, help="Guardar checkpoint cada N epocas (PyTorch)")
    p.add_argument("--backend", choices=["auto", "torch", "sklearn"], default="auto", help="Forzar backend")
    p.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto", help="Seleccionar dispositivo (solo PyTorch)")
    p.add_argument("--seed", type=int, default=None, help="Semilla para reproducibilidad (numpy, random, torch)")
    p.add_argument("--resume", type=str, default=None, help="Ruta al checkpoint para reanudar (PyTorch)")
    p.add_argument("--tb", action="store_true", help="Activar logging a TensorBoard (solo PyTorch)")
    p.add_argument("--val-size", type=float, default=0.1, help="Fracción del dataset para validación (por defecto 0.1)")
    p.add_argument("--patience", type=int, default=3, help="Paciencia para early stopping (número de epochs sin mejora)")
    p.add_argument("--monitor", choices=["accuracy", "loss"], default="accuracy", help="Métrica a monitorizar para early stopping y guardado de mejor modelo")
    return p.parse_args()


def main():
    args = parse_args()
    X_train, X_val, X_test, y_train, y_val, y_test = load_data(test_size=0.2, val_size=args.val_size)

    # decidir backend
    backend = args.backend
    if backend == "auto":
        use_torch = USE_TORCH
    else:
        use_torch = (backend == "torch") and USE_TORCH

    # establecer semilla si se pide
    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)
        try:
            import torch as _torch
            _torch.manual_seed(args.seed)
            _torch.cuda.manual_seed_all(args.seed)
        except Exception:
            pass

    # resolver dispositivo
    device = None
    if args.device != "auto":
        if args.device == "cpu":
            device = (torch.device("cpu") if USE_TORCH else None)
        elif args.device == "cuda":
            device = (torch.device("cuda") if USE_TORCH and torch.cuda.is_available() else (torch.device("cpu") if USE_TORCH else None))

    if use_torch:
        # Si se solicita TensorBoard y está disponible, crear SummaryWriter
        tb_writer = None
        if args.tb:
            try:
                from torch.utils.tensorboard import SummaryWriter
                tb_writer = SummaryWriter(log_dir=(args.save_dir if args.save_dir else "runs"))
                print(f"TensorBoard activo en: {args.save_dir if args.save_dir else 'runs'}")
            except Exception:
                print("TensorBoard no disponible (instala 'tensorboard' si quieres usar --tb)")

        train_torch(X_train, X_val, X_test, y_train, y_val, y_test, epochs=args.epochs, batch_size=args.batch_size, lr=args.lr, save_dir=args.save_dir, save_every=args.save_every, device=device, resume_path=args.resume, tb_writer=tb_writer, patience=args.patience, monitor=args.monitor)
        if tb_writer is not None:
            tb_writer.close()
    else:
        # Para sklearn también pasamos validation set y TensorBoard writer opcional
        tb_writer = None
        if args.tb:
            try:
                from torch.utils.tensorboard import SummaryWriter
                tb_writer = SummaryWriter(log_dir=(args.save_dir if args.save_dir else "runs"))
                print(f"TensorBoard activo en: {args.save_dir if args.save_dir else 'runs'}")
            except Exception:
                print("TensorBoard no disponible (instala 'tensorboard' si quieres usar --tb)")

        train_sklearn(X_train, X_val, X_test, y_train, y_val, y_test, save_dir=args.save_dir, patience=args.patience, monitor=args.monitor, tb_writer=tb_writer)
        if tb_writer is not None:
            tb_writer.close()


if __name__ == "__main__":
    main()
