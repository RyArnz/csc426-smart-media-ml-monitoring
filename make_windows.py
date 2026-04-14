from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description="Create supervised windows from processed CSV files.")
    parser.add_argument("--processed-dir", type=str, default="data/processed", help="Processed data directory")
    parser.add_argument("--window-size", type=int, default=60, help="Number of past steps per sample")
    return parser.parse_args()


def create_windows(df: pd.DataFrame, feature_cols, target_col, window_size: int):
    X, y, timestamps = [], [], []

    feature_values = df[feature_cols].to_numpy(dtype=np.float32)
    target_values = df[target_col].to_numpy(dtype=np.float32)
    time_values = df["timestamp"].astype(str).to_list()

    for i in range(window_size, len(df)):
        X.append(feature_values[i - window_size:i])
        y.append(target_values[i])
        timestamps.append(time_values[i])

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32), np.array(timestamps)


def main():
    args = parse_args()
    processed_dir = Path(args.processed_dir)

    with open(processed_dir / "metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    feature_cols = metadata["feature_cols"]
    target_col = metadata["target_col"]

    train_df = pd.read_csv(processed_dir / "train_scaled.csv")
    val_df = pd.read_csv(processed_dir / "val_scaled.csv")
    test_df = pd.read_csv(processed_dir / "test_scaled.csv")

    X_train, y_train, t_train = create_windows(train_df, feature_cols, target_col, args.window_size)
    X_val, y_val, t_val = create_windows(val_df, feature_cols, target_col, args.window_size)
    X_test, y_test, t_test = create_windows(test_df, feature_cols, target_col, args.window_size)

    np.save(processed_dir / "X_train.npy", X_train)
    np.save(processed_dir / "y_train.npy", y_train)
    np.save(processed_dir / "X_val.npy", X_val)
    np.save(processed_dir / "y_val.npy", y_val)
    np.save(processed_dir / "X_test.npy", X_test)
    np.save(processed_dir / "y_test.npy", y_test)

    np.save(processed_dir / "t_train.npy", t_train)
    np.save(processed_dir / "t_val.npy", t_val)
    np.save(processed_dir / "t_test.npy", t_test)

    metadata["window_size"] = args.window_size
    metadata["X_train_shape"] = list(X_train.shape)
    metadata["X_val_shape"] = list(X_val.shape)
    metadata["X_test_shape"] = list(X_test.shape)

    with open(processed_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("Window creation complete.")
    print("X_train:", X_train.shape, "y_train:", y_train.shape)
    print("X_val:  ", X_val.shape, "y_val:  ", y_val.shape)
    print("X_test: ", X_test.shape, "y_test: ", y_test.shape)


if __name__ == "__main__":
    main()
