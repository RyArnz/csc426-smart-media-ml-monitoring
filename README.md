# CSC 426 Deep Learning – Smart Media Server ML Monitoring

This project builds a practical deep learning pipeline for monitoring a smart home media server using Prometheus telemetry.

## Project Goal

The goal of this project is to use machine learning and deep learning to monitor media server behavior and predict future system load. The current milestone focuses on **multivariate time-series forecasting** rather than classification.

### Current prediction task
- **Input:** previous 60 minutes of server telemetry
- **Output:** next 10-minute average CPU usage

This creates a foundation for later predictive maintenance features such as overload warnings, anomaly detection, or maintenance-risk classification.

## Current Pipeline

The working pipeline is:

1. Pull historical server metrics from **Prometheus**
2. Preprocess and clean the exported CSV
3. Convert the time series into equal-length supervised windows
4. Train deep learning models in TensorFlow/Keras
5. Evaluate forecasting performance

## Data Source

Metrics are collected from Prometheus using the Prometheus HTTP API.

### Current Prometheus queries include:
- server CPU percent
- server RAM percent
- disk usage percent
- container RAM usage
- container CPU usage
- container count

### Example collected columns
- `timestamp`
- `server_cpu_percent`
- `server_ram_percent`
- `disk_usage_percent`
- `container_ram_mb`
- `container_cpu_cores`
- `container_count`

## Current Dataset

For the current milestone run, data was pulled from:

- **Start:** 2026-04-07T00:00:00Z
- **End:** 2026-04-14T00:00:00Z
- **Step:** 60 seconds

This produced:

- **10,081 rows**
- **7 columns**
- no missing values in the exported dataset

## Preprocessing

The preprocessing stage:

- parses and sorts timestamps
- renames columns into cleaner model feature names
- resamples to a fixed interval
- creates the target as the future 10-minute average CPU usage
- splits the data by **time order**
- scales features using **training-set statistics only**

### Final split sizes
- Train rows: 7,051
- Validation rows: 1,510
- Test rows: 1,510

## Windowing

The processed data is converted into supervised time-series windows.

### Current window configuration
- **Window size:** 60
- **Forecast horizon:** 10

### Final supervised dataset shapes
- `X_train`: `(6991, 60, 6)`
- `X_val`: `(1450, 60, 6)`
- `X_test`: `(1450, 60, 6)`

## Models

Two TensorFlow/Keras models are implemented.

### 1. Baseline model: MLP
Architecture:
- Flatten
- Dense(64, relu)
- Dense(32, relu)
- Dense(1)

### 2. Primary model: LSTM
Architecture:
- LSTM(64)
- Dropout(0.2)
- Dense(16, relu)
- Dense(1)

## Results

### Most recent comparable training run

| Model | Test MSE | Test MAE | Test RMSE |
|---|---:|---:|---:|
| MLP | 0.0032 | 0.0440 | 0.0561 |
| LSTM | 0.0021 | 0.0367 | 0.0453 |

The LSTM outperformed the MLP on all reported test metrics.

### Best saved evaluated LSTM run
- MSE: **0.0016**
- MAE: **0.0317**
- RMSE: **0.0402**

## Repository Files

### Core scripts
- `pull_from_prometheus.py` – pulls metrics from Prometheus into CSV
- `preprocess.py` – cleans and prepares the dataset
- `make_windows.py` – converts processed data into supervised windows
- `models.py` – defines the MLP and LSTM models
- `train.py` – trains the selected model
- `evaluate.py` – evaluates a saved model and generates plots

### Supporting files
- `requirements.txt` – full project dependencies
- `requirements_scrape.txt` – lightweight scrape/preprocess dependencies
- `Milestone 1.md`
- `Milestone 2 Progress`
- `Milestone 3.md`

## How to Run

### 1. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
