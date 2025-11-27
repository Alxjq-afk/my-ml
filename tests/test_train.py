import numpy as np
from train import train_sklearn, load_data


def test_train_sklearn_quick():
    # load small subset
    X_train, X_val, X_test, y_train, y_val, y_test = load_data(test_size=0.2, val_size=0.1)
    # take a small subset to make test fast
    Xtr = X_train[:80]
    ytr = y_train[:80]
    Xv = X_val[:20] if X_val is not None else None
    yv = y_val[:20] if y_val is not None else None
    Xt = X_test[:20]
    yt = y_test[:20]

    # Run with small patience to stop quickly
    train_sklearn(Xtr, Xv, Xt, ytr, yv, yt, save_dir=None, patience=1, monitor='accuracy', tb_writer=None)
    # If no exception, consider test passed
    assert True
