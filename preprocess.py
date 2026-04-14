from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd


FEATURE_RENAME_MAP = {
    "server_cpu_percent": "cpu_percent",
    "server_ram_percent": "ram_percent",
    "disk_usage_percent": "disk_percent",
    "container_ram_mb": "container_ram_mb",
    "container_cpu_cores": "container_cpu_cores",
    "container_count": "container_count",
}


def parse_args():
    parser = argparse.ArgumentParser(description="Preprocess Prometheus CSV for ML training.")
    parser.add_argument("--input", type=str, required=True, help="Input raw CSV path")
    parser.add_argument("--output-dir", type=str, default="data/processed", help="Output directory")
    parser.add_argument("--resample-rule", type=str, default="1min", help="Resample interval")
    parser.add_argument("--target-col", type=str, default="cpu_percent", help="Target feature after renaming")
    parser.add_argument("--forecast-horizon", type=int, default=10, help="Future horizon in steps")
    parser.add_argument("--val-ratio", type=float, default=0.15, help="Validation ratio")
    parser.add_argument("--test-ratio", type=float, default=0.15, help="Test ratio")
    return parser.parse_args()


def time_split(df: pd.DataFrame, val_ratio: float, test_ratio: float):
    n = len(df)
    test_size = int(n * test_ratio)
    val_size = int(n * val_ratio)
    train_size = n - val_size - test_size

    train_df = df.iloc[:train_size].copy()
    val_df = df.iloc[train_size:train_size + val_size].copy()
    test_df = df.iloc[train_size + val_size:].copy()

    return train_df, val_df, test_df


def compute_scaler_stats(train_df: pd.DataFrame, feature_cols):
    means = train_df[feature_cols].mean()
    stds = train_df[feature_cols].std().replace(0, 1.0)
    return means, stds


def scale_split(df: pd.DataFrame, feature_cols, means, stds):
    out = df.copy()
    out[feature_cols] = (out[feature_cols] - means) / stds
    return out


def main():
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    # Parse and sort timestamps
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df.sort_values("timestamp").drop_duplicates(subset=["timestamp"]).reset_index(drop=True)

    # Rename columns to cleaner training names
    df = df.rename(columns=FEATURE_RENAME_MAP)

    # Keep only expected columns if present
    feature_cols = [c for c in FEATURE_RENAME_MAP.values() if c in df.columns]

    # Set timestamp index for resampling
    df = df.set_index("timestamp")

    # Resample to fixed interval
    df = df.resample(args.resample_rule).mean()

    # Fill missing values conservatively
    df = df.ffill().bfill()

    # Create target: next forecast_horizon-step average CPU usage
    target_col = args.target_col
    future_avg_target_name = f"target_future_{args.forecast_horizon}min_avg_cpu"

    df[future_avg_target_name] = (
        df[target_col]
        .shift(-1)
        .rolling(window=args.forecast_horizon, min_periods=args.forecast_horizon)
        .mean()
        .shift(-(args.forecast_horizon - 1))
    )

    # Drop rows with incomplete target
    df = df.dropna().reset_index()

    # Split by time order
    train_df, val_df, test_df = time_split(df, args.val_ratio, args.test_ratio)

    # Fit scaler on training only
    means, stds = compute_scaler_stats(train_df, feature_cols)

    # Scale features only
    train_scaled = scale_split(train_df, feature_cols, means, stds)
    val_scaled = scale_split(val_df, feature_cols, means, stds)
    test_scaled = scale_split(test_df, feature_cols, means, stds)

    # Save outputs
    train_scaled.to_csv(output_dir / "train_scaled.csv", index=False)
    val_scaled.to_csv(output_dir / "val_scaled.csv", index=False)
    test_scaled.to_csv(output_dir / "test_scaled.csv", index=False)

    # Also save unscaled full cleaned frame for inspection
    df.to_csv(output_dir / "clean_full.csv", index=False)

    metadata = {
        "feature_cols": feature_cols,
        "target_col": future_avg_target_name,
        "resample_rule": args.resample_rule,
        "forecast_horizon": args.forecast_horizon,
        "train_rows": len(train_scaled),
        "val_rows": len(val_scaled),
        "test_rows": len(test_scaled),
        "input_path": str(input_path),
    }

    with open(output_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("Preprocessing complete.")
    print("Features:", feature_cols)
    print("Target:", future_avg_target_name)
    print("Train rows:", len(train_scaled))
    print("Val rows:", len(val_scaled))
    print("Test rows:", len(test_scaled))
    print(f"Saved outputs to: {output_dir}")


if __name__ == "__main__":
    main()
