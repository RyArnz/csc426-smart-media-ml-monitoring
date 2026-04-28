from pathlib import Path
import argparse
import json
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras

from models import build_mlp, build_lstm


def parse_args():
    parser = argparse.ArgumentParser(description="Train MLP or LSTM on Prometheus windows.")
    parser.add_argument("--processed-dir", type=str, default="data/processed")
    parser.add_argument("--model-name", type=str, choices=["mlp", "lstm"], default="lstm")
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--lstm-units", type=int, default=64)
    parser.add_argument("--dropout", type=float, default=0.2)
    return parser.parse_args()


def plot_history(history, output_path: Path):
    plt.figure(figsize=(10, 5))
    plt.plot(history.history["loss"], label="train_loss")
    plt.plot(history.history["val_loss"], label="val_loss")
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.title("Training vs Validation Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main():
    args = parse_args()
    processed_dir = Path(args.processed_dir)

    X_train = np.load(processed_dir / "X_train.npy")
    y_train = np.load(processed_dir / "y_train.npy")
    X_val = np.load(processed_dir / "X_val.npy")
    y_val = np.load(processed_dir / "y_val.npy")
    X_test = np.load(processed_dir / "X_test.npy")
    y_test = np.load(processed_dir / "y_test.npy")

    with open(processed_dir / "metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    input_shape = X_train.shape[1:]

    if args.model_name == "mlp":
        model = build_mlp(
            input_shape=input_shape,
            learning_rate=args.learning_rate,
        )
    else:
        model = build_lstm(
            input_shape=input_shape,
            lstm_units=args.lstm_units,
            dropout=args.dropout,
            learning_rate=args.learning_rate,
        )

    run_name = f"{args.model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    model_dir = Path("artifacts/models") / run_name
    plots_dir = model_dir / "plots"
    model_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)

    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
        ),
        keras.callbacks.ModelCheckpoint(
            filepath=str(model_dir / "best_model.keras"),
            monitor="val_loss",
            save_best_only=True,
        ),
    ]

    print("\nModel summary:")
    model.summary()

    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=args.epochs,
        batch_size=args.batch_size,
        callbacks=callbacks,
        verbose=1,
    )

    test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
    test_rmse = float(np.sqrt(test_loss))

    model.save(model_dir / "final_model.keras")

    history_dict = {k: [float(v) for v in vals] for k, vals in history.history.items()}
    with open(model_dir / "history.json", "w", encoding="utf-8") as f:
        json.dump(history_dict, f, indent=2)

    run_metadata = {
        "run_name": run_name,
        "model_name": args.model_name,
        "input_shape": list(input_shape),
        "X_train_shape": list(X_train.shape),
        "X_val_shape": list(X_val.shape),
        "X_test_shape": list(X_test.shape),
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "learning_rate": args.learning_rate,
        "lstm_units": args.lstm_units,
        "dropout": args.dropout,
        "test_mse": float(test_loss),
        "test_mae": float(test_mae),
        "test_rmse": test_rmse,
        "feature_cols": metadata["feature_cols"],
        "target_col": metadata["target_col"],
        "window_size": metadata["window_size"],
    }

    with open(model_dir / "run_metadata.json", "w", encoding="utf-8") as f:
        json.dump(run_metadata, f, indent=2)

    plot_history(history, plots_dir / "learning_curves.png")

    print(f"\nTraining complete for {args.model_name}")
    print(f"Saved to: {model_dir}")
    print(f"Test MSE:  {test_loss:.4f}")
    print(f"Test MAE:  {test_mae:.4f}")
    print(f"Test RMSE: {test_rmse:.4f}")

    print("\nInterpretation:")
    print("- If validation loss stays close to training loss, the model is generalizing reasonably well.")
    print("- If training loss drops much lower than validation loss, that suggests overfitting.")
    print("- If both losses remain high, that suggests underfitting.")


if __name__ == "__main__":
    main()
