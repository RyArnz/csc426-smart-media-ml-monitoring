from pathlib import Path
import argparse
import json

import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate a trained model run.")
    parser.add_argument("--model-dir", type=str, required=True, help="Path to saved model run folder")
    parser.add_argument("--processed-dir", type=str, default="data/processed")
    return parser.parse_args()


def main():
    args = parse_args()
    model_dir = Path(args.model_dir)
    processed_dir = Path(args.processed_dir)
    plots_dir = model_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    X_test = np.load(processed_dir / "X_test.npy")
    y_test = np.load(processed_dir / "y_test.npy")
    t_test = np.load(processed_dir / "t_test.npy", allow_pickle=True)

    model = keras.models.load_model(model_dir / "best_model.keras")

    preds = model.predict(X_test, verbose=0).reshape(-1)

    mse = float(np.mean((y_test - preds) ** 2))
    mae = float(np.mean(np.abs(y_test - preds)))
    rmse = float(np.sqrt(mse))
    residuals = y_test - preds

    metrics = {
        "mse": mse,
        "mae": mae,
        "rmse": rmse,
    }

    with open(model_dir / "evaluation_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    np.save(model_dir / "predictions.npy", preds)
    np.save(model_dir / "residuals.npy", residuals)

    plt.figure(figsize=(12, 5))
    plt.plot(y_test[:300], label="actual")
    plt.plot(preds[:300], label="predicted")
    plt.xlabel("Test sample")
    plt.ylabel("Future avg CPU target")
    plt.title("Actual vs Predicted (first 300 test samples)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(plots_dir / "actual_vs_predicted.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.hist(residuals, bins=30)
    plt.xlabel("Residual")
    plt.ylabel("Frequency")
    plt.title("Residual Histogram")
    plt.tight_layout()
    plt.savefig(plots_dir / "residual_histogram.png")
    plt.close()

    summary_path = model_dir / "evaluation_summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("Model Evaluation Summary\n")
        f.write("========================\n")
        f.write(f"MSE:  {mse:.6f}\n")
        f.write(f"MAE:  {mae:.6f}\n")
        f.write(f"RMSE: {rmse:.6f}\n\n")
        f.write("Interpretation:\n")
        f.write("- Lower MAE means predictions are closer to the true future average CPU usage.\n")
        f.write("- RMSE penalizes larger errors more strongly than MAE.\n")
        f.write("- A wide residual spread suggests unstable forecasts.\n")
        f.write("- Residuals centered near zero suggest less bias.\n")

    print("\nEvaluation complete.")
    print(f"MSE:  {mse:.4f}")
    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"Saved evaluation outputs to: {model_dir}")


if __name__ == "__main__":
    main()
