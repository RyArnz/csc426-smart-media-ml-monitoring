# CSC 426 Deep Learning – Smart Media Server ML Monitoring

This repository contains a complete deep learning project for monitoring a smart home media server using real Prometheus telemetry. The project collects server metrics, analyzes the dataset, preprocesses the data into supervised time-series windows, trains neural network forecasting models, evaluates results, and saves plots/model artifacts for reporting.

The main project idea is to move from **reactive monitoring** to **short-term predictive maintenance**. Instead of only seeing that CPU, RAM, or container load is high right now, the system learns from recent server behavior and forecasts near-future CPU load.

---

## Project Title

**AI-Driven Monitoring and Predictive Maintenance on a Smart Home Media Server**

---

## Team Members

- **Ryan Arnzen**
- **Prasiddha Neupane**

---

## Project Summary

Smart home media servers often run several services at the same time, such as media streaming, cloud storage, reverse proxy services, monitoring tools, and Docker containers. These systems can become overloaded when CPU, RAM, disk, or container activity increases.

This project builds a practical machine learning pipeline that uses server telemetry to predict short-term CPU load. The current project focuses on **multivariate time-series forecasting**.

### Current prediction task

- **Input:** recent server telemetry from the previous 30 or 60 minutes
- **Output:** the next 10-minute average CPU usage
- **Model type:** supervised regression
- **Primary model:** LSTM
- **Baseline model:** MLP

The strongest result came from the **30-minute LSTM model**, which produced the lowest test error in the final experiment comparison.

---

## Why This Project Matters

Traditional monitoring tools show what is happening right now. This project explores whether deep learning can help estimate what may happen next.

A future version of this project could support:

- overload warnings
- predictive maintenance alerts
- anomaly detection
- automatic maintenance triggers
- health-score classification
- real-time Grafana dashboard integration
- containerized ML inference

The current version is an offline training and evaluation pipeline. It does **not** yet run live predictions continuously against the server, but it establishes the model, data pipeline, and evaluation artifacts needed to build that next step.

---

## Deep Learning Problem Type

This project is a **multivariate time-series regression** problem.

| Concept | Meaning in this project |
|---|---|
| Supervised learning | The model trains using known input windows and known future CPU labels |
| Regression | The model predicts a numeric CPU value |
| Time-series forecasting | The input data is ordered by timestamp and used to predict future behavior |
| Multivariate input | Multiple server metrics are used as input features |
| Target variable | The future 10-minute average CPU usage |
| Sliding window | A fixed block of recent server readings used as one training example |

---

## Server Monitoring Stack

The telemetry comes from a smart media server monitoring setup.

### Main monitoring components

| Tool | Role |
|---|---|
| Prometheus | Collects and stores time-series metrics |
| Prometheus HTTP API | Used by Python scripts to export metric data |
| node-exporter | Provides host-level CPU, RAM, disk, and system metrics |
| cAdvisor | Provides Docker/container-level CPU and memory metrics |
| Docker | Runs the media server services and monitoring services |
| Grafana | Used for visualization of server monitoring data |
| Python | Used for data export, preprocessing, model training, and evaluation |
| TensorFlow/Keras | Used to build and train deep learning models |

---

## Data Source

Metrics are collected from Prometheus using the Prometheus HTTP API.

The main raw dataset is:

```text
data/raw/prometheus_week.csv
```

### Current Prometheus Metrics Collected

The project collects these server and container measurements:

- server CPU percent
- server RAM percent
- disk usage percent
- container RAM usage
- container CPU usage
- container count

### Raw Collected Columns

```text
timestamp
server_cpu_percent
server_ram_percent
disk_usage_percent
container_ram_mb
container_cpu_cores
container_count
```

---

## Current Dataset

For the final project run, telemetry was pulled from:

| Field | Value |
|---|---|
| Start | 2026-04-07T00:00:00Z |
| End | 2026-04-14T00:00:00Z |
| Step | 60 seconds |
| Rows | 10,081 |
| Columns | 7 |
| Missing values | 0 |

This represents one week of server telemetry at a one-minute interval.

---

## Feature Columns and Target Variable

The model uses multiple input features, but predicts one target value.

### Input Features

After preprocessing, the model feature columns are:

```text
cpu_percent
ram_percent
disk_percent
container_ram_mb
container_cpu_cores
container_count
```

These are the values the model is allowed to use when learning patterns.

### Target Variable

The target column is:

```text
target_future_10min_avg_cpu
```

The target is one value: the average CPU usage over the next 10 minutes.

Formula:

```text
target_t = mean(cpu_{t+1}, ..., cpu_{t+10})
```

This means that for each time point `t`, the label is the average of the next 10 actual CPU readings.

Using a 10-minute average smooths out small one-minute spikes and gives a more useful short-term server-load target.

---

## Dataset Statistics

The final dataset showed mostly stable, low-load server behavior.

| Metric | Mean | Std | Min | Max |
|---|---:|---:|---:|---:|
| CPU % | 1.168 | 0.104 | 0.864 | 3.514 |
| RAM % | 12.611 | 0.149 | 12.067 | 13.818 |
| Disk % | 20.473 | 0.010 | 20.366 | 20.496 |
| Container RAM MB | 1749.203 | 21.196 | 1672.477 | 1831.941 |
| Container CPU cores | 0.082 | 0.006 | 0.063 | 0.107 |
| Container count | 10.000 | 0.000 | 10.000 | 10.000 |

### Important Dataset Observations

- CPU usage stayed low and stable during the collection period.
- RAM and disk usage were also stable.
- Container CPU had visible minute-to-minute movement.
- Container count stayed fixed at 10, so it did not provide useful variation for learning.
- Because the dataset has low variance, the model performs well on normal server behavior, but the current results should not be interpreted as proof that the model handles heavy overload or failure conditions.

---

## Preprocessing Pipeline

The preprocessing stage converts the raw Prometheus export into a clean time-series dataset for model training.

Implemented in:

```text
preprocess.py
```

### Preprocessing Steps

1. Load the raw Prometheus CSV.
2. Parse the `timestamp` column.
3. Sort all rows in chronological order.
4. Remove duplicate timestamps.
5. Rename raw columns into cleaner feature names.
6. Resample the dataset to a fixed one-minute interval.
7. Fill short gaps with forward-fill and backward-fill.
8. Create the future 10-minute average CPU target.
9. Drop rows that cannot have a complete future target.
10. Split the data by time order into training, validation, and test sets.
11. Scale features using training-set statistics only.
12. Save processed CSV files, NumPy arrays, and metadata.

### Missing Value Strategy

The raw export contained no missing values, but the preprocessing pipeline still includes gap handling after resampling.

The pipeline uses:

```text
forward-fill followed by backward-fill
```

This means:

- if a value is missing, use the previous known value
- if a missing value occurs at the very beginning, use the next available value

This keeps the time series continuous for sliding-window generation.

### Scaling Strategy

The feature columns are standardized using training-set statistics only.

Formula:

```text
x_scaled = (x - training_mean) / training_standard_deviation
```

This prevents data leakage because validation and test statistics are not used to fit the scaler.

The target column remains in CPU-percent units so MAE and RMSE remain interpretable.

### Final Split Sizes

| Split | Rows |
|---|---:|
| Training | 7,051 |
| Validation | 1,510 |
| Test | 1,510 |

The split is time-based, not random. Earlier data is used for training, the middle section is used for validation, and the latest section is used for final testing.

---

## Windowing

Implemented in:

```text
make_windows.py
```

The processed rows are converted into supervised time-series windows.

For a 60-minute window, each sample contains:

```text
60 time steps × 6 features
```

For a 30-minute window, each sample contains:

```text
30 time steps × 6 features
```

### Main 60-Minute Supervised Dataset Shapes

```text
X_train: (6991, 60, 6)
X_val:   (1450, 60, 6)
X_test:  (1450, 60, 6)
```

### 30-Minute Experiment Dataset Shapes

```text
X_train: (7021, 30, 6)
X_val:   (1480, 30, 6)
X_test:  (1480, 30, 6)
```

### What These Shapes Mean

For the 60-minute experiment:

```text
6991 training samples
60 minutes per sample
6 features per minute
```

Each `X` sample is a recent history window. Each matching `y` value is the future 10-minute average CPU usage.

---

## Models

The project implements two TensorFlow/Keras models in:

```text
models.py
```

---

### 1. Baseline Model: MLP

The MLP is a feedforward neural network baseline.

Architecture:

```text
Flatten(60×6) → Dense(64, ReLU) → Dense(32, ReLU) → Dense(1)
```

Trainable parameters:

```text
25,217
```

### What the MLP Does

The MLP flattens the time window into one long vector. For a 60-minute window with 6 features:

```text
60 × 6 = 360 input values
```

The MLP can learn relationships between recent metrics, but it does not explicitly process them as an ordered sequence.

The MLP answers this question:

```text
Can a non-sequential neural network learn useful patterns from recent server metrics?
```

---

### 2. Primary Model: LSTM

The LSTM is the primary sequence model.

Architecture:

```text
LSTM(64) → Dropout(0.2) → Dense(16, ReLU) → Dense(1)
```

Trainable parameters:

```text
19,233
```

### What the LSTM Does

The LSTM processes server telemetry in time order. It reads the window as a sequence, minute by minute.

This makes it better suited for time-series forecasting because server behavior often depends on trends over time.

Example patterns the LSTM may learn:

- container CPU rising over several minutes
- CPU staying stable for a long period
- RAM or container RAM gradually increasing
- short-term workload movement that affects future CPU

### Dropout Explanation

`Dropout(0.2)` randomly disables 20% of the LSTM output values during training. This helps reduce overfitting by preventing the model from relying too heavily on one internal pathway.

Dropout is only active during training. It is not used during final evaluation or prediction.

---

## Training Configuration

Implemented in:

```text
train.py
```

Both models use:

| Setting | Value |
|---|---|
| Optimizer | Adam |
| Loss function | Mean Squared Error |
| Metric | Mean Absolute Error |
| Validation monitoring | Validation loss |
| Early stopping patience | 5 epochs |
| Checkpointing | Best model saved by validation loss |

### Evaluation Metrics

The project reports:

```text
MSE
MAE
RMSE
```

Formula summary:

```text
MSE  = (1/n) Σ(yᵢ - ŷᵢ)²
MAE  = (1/n) Σ|yᵢ - ŷᵢ|
RMSE = √MSE
```

### What Each Metric Means

| Metric | Meaning |
|---|---|
| MSE | Average squared prediction error; penalizes larger mistakes more heavily |
| MAE | Average absolute error in CPU percentage-point units |
| RMSE | Square root of MSE; easier to interpret than MSE and still sensitive to larger mistakes |

---

## Final Results

The final experiment comparison tested three settings:

1. MLP baseline with 60-minute window
2. LSTM primary model with 60-minute window
3. LSTM shorter-window model with 30-minute window

| Experiment | Test MSE | Test MAE | Test RMSE |
|---|---:|---:|---:|
| MLP 60-min | 0.003684 | 0.048503 | 0.060694 |
| LSTM 60-min | 0.001227 | 0.028447 | 0.035034 |
| LSTM 30-min | 0.001000 | 0.026000 | 0.031600 |

### Main Finding

The **30-minute LSTM** had the lowest test error.

The 60-minute LSTM reduced RMSE by about 42% compared with the MLP baseline. The 30-minute LSTM improved again, suggesting that the most recent half-hour of telemetry was enough context for this stable server workload.

### Interpretation

The LSTM models outperformed the MLP baseline, which supports the idea that the order of server readings provides useful forecasting information.

Because the server was mostly under low load, these results are best interpreted as strong performance on stable server behavior, not as proof that the model can already predict overload or failure states.

---

## Output Artifacts

The project saves model and reporting artifacts under:

```text
artifacts/
```

### Important Artifact Types

- dataset overview reports
- dataset statistics tables
- column type and missing value tables
- EDA plots
- feature correlation heatmaps
- trained Keras model checkpoints
- training history JSON files
- learning curves
- actual-vs-predicted plots
- residual arrays
- residual histograms
- model comparison CSV files
- final summary text files

---

## Repository Structure

```text
.
├── artifacts/
│   ├── figures/
│   ├── final_results/
│   ├── models/
│   ├── reports/
│   └── tables/
├── data/
│   ├── raw/
│   ├── processed/
│   └── processed_window30/
├── analyze_dataset.py
├── evaluate.py
├── generate_experiment_comparison.py
├── generate_final_results.py
├── make_windows.py
├── models.py
├── preprocess.py
├── pull_from_prometheus.py
├── train.py
├── README.md
├── Milestone 1.md
├── Milestone 2 Progress
├── milestone 3.md
├── requirements_scrape.txt
└── .gitignore
```

---

## Repository Files Explained

### Core Scripts

| File | Purpose |
|---|---|
| `pull_from_prometheus.py` | Pulls historical server metrics from Prometheus into CSV format |
| `analyze_dataset.py` | Performs exploratory data analysis and creates dataset plots/tables |
| `preprocess.py` | Cleans the raw CSV, creates the target, splits data, and scales features |
| `make_windows.py` | Converts processed rows into supervised time-series windows |
| `models.py` | Defines the MLP and LSTM TensorFlow/Keras models |
| `train.py` | Trains a selected model and saves checkpoints/artifacts |
| `evaluate.py` | Evaluates a saved model and creates predictions/residual plots |
| `generate_final_results.py` | Creates final MLP vs LSTM comparison outputs |
| `generate_experiment_comparison.py` | Creates the three-experiment comparison charts and tables |

### Data Files

| File or folder | Purpose |
|---|---|
| `data/raw/prometheus_week.csv` | Main raw one-week Prometheus export |
| `data/processed/clean_full.csv` | Cleaned full dataset with target column |
| `data/processed/train_scaled.csv` | Scaled training split |
| `data/processed/val_scaled.csv` | Scaled validation split |
| `data/processed/test_scaled.csv` | Scaled test split |
| `data/processed/X_train.npy` | Training input windows |
| `data/processed/y_train.npy` | Training target values |
| `data/processed/X_val.npy` | Validation input windows |
| `data/processed/y_val.npy` | Validation target values |
| `data/processed/X_test.npy` | Test input windows |
| `data/processed/y_test.npy` | Test target values |
| `data/processed/metadata.json` | Metadata about features, target, splits, and window shape |
| `data/processed_window30/` | Processed files for the 30-minute LSTM experiment |

### Report and Milestone Files

| File | Purpose |
|---|---|
| `Milestone 1.md` | Initial project proposal and motivation |
| `Milestone 2 Progress` | Data collection and preprocessing progress |
| `milestone 3.md` | Deep learning model development and training report |

---

## How to Run

The commands below assume a Linux or macOS-style terminal.

---

### 1. Clone the Repository

```bash
git clone https://github.com/RyArnz/csc426-smart-media-ml-monitoring.git
cd csc426-smart-media-ml-monitoring
```

---

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

### 3. Install Dependencies

For lightweight scraping/preprocessing:

```bash
pip install -r requirements_scrape.txt
```

For full model training, TensorFlow/Keras is also required. If TensorFlow is not already installed, install it:

```bash
pip install tensorflow
```

Optional full install command:

```bash
pip install pandas numpy requests python-dotenv matplotlib scikit-learn tensorflow
```

---

## Running the Pipeline

### 1. Pull Data from Prometheus

Example:

```bash
python pull_from_prometheus.py \
  --base-url http://YOUR_PROMETHEUS_HOST:9090 \
  --start 2026-04-07T00:00:00Z \
  --end 2026-04-14T00:00:00Z \
  --step 60s \
  --output data/raw/prometheus_week.csv
```

If the dataset is already included, this step can be skipped.

---

### 2. Analyze the Dataset

```bash
python analyze_dataset.py
```

This creates dataset reports, tables, and plots under:

```text
artifacts/
```

---

### 3. Preprocess the Dataset

For the main 60-minute experiment:

```bash
python preprocess.py \
  --input data/raw/prometheus_week.csv \
  --output-dir data/processed \
  --forecast-horizon 10 \
  --resample-rule 1min
```

---

### 4. Create 60-Minute Windows

```bash
python make_windows.py \
  --processed-dir data/processed \
  --window-size 60
```

---

### 5. Train the MLP Baseline

```bash
python train.py \
  --processed-dir data/processed \
  --model-name mlp \
  --epochs 50 \
  --batch-size 32
```

---

### 6. Train the LSTM Model

```bash
python train.py \
  --processed-dir data/processed \
  --model-name lstm \
  --epochs 50 \
  --batch-size 32 \
  --lstm-units 64 \
  --dropout 0.2
```

---

### 7. Evaluate a Saved Model

Replace the model directory with the folder created by training.

```bash
python evaluate.py \
  --model-dir artifacts/models/YOUR_MODEL_RUN_FOLDER
```

---

### 8. Run the 30-Minute Window Experiment

Create a second processed dataset folder:

```bash
python preprocess.py \
  --input data/raw/prometheus_week.csv \
  --output-dir data/processed_window30 \
  --forecast-horizon 10 \
  --resample-rule 1min
```

Create 30-minute windows:

```bash
python make_windows.py \
  --processed-dir data/processed_window30 \
  --window-size 30
```

Train the 30-minute LSTM:

```bash
python train.py \
  --processed-dir data/processed_window30 \
  --model-name lstm \
  --epochs 50 \
  --batch-size 32 \
  --lstm-units 64 \
  --dropout 0.2
```

---

### 9. Generate Final Comparison Outputs

```bash
python generate_final_results.py
python generate_experiment_comparison.py
```

These scripts create final result tables and plots under:

```text
artifacts/final_results/
```

---

## What the Current Model Does

The current model is an **offline forecasting model**.

It loads saved processed arrays, trains models, evaluates on a held-out test split, and saves prediction artifacts.

Current behavior:

- trains on historical Prometheus data
- evaluates on the newest held-out test portion
- saves test predictions
- saves residuals
- generates plots and metrics
- compares MLP and LSTM model results

The current code does **not** yet continuously query Prometheus for live inference.

---

## What “Current Data” Means in This Project

In this project, “current data” usually refers to the most recent part of the collected historical dataset.

The test split is:

```text
the final 15% of the saved historical Prometheus export
```

It is not live server data from the current moment.

The test set simulates how the model would perform on future server behavior because it uses later timestamps that were not used during training.

---

## Future Live Deployment Plan

A future production version would add an inference service.

The live workflow would be:

```text
Prometheus
    ↓
Python inference container
    ↓
Load latest 30/60 minutes of metrics
    ↓
Apply same preprocessing and scaling
    ↓
Load best_model.keras
    ↓
Predict future 10-minute average CPU
    ↓
Send result to logs, Grafana, alerts, or dashboard
```

### Future Deployment Idea

The model could be deployed as a Docker container that:

- queries Prometheus every few minutes
- builds the latest sliding window
- scales data using saved training scaler values
- loads the saved Keras model
- predicts future CPU usage
- writes predictions to a file, database, API endpoint, or Prometheus exporter
- triggers warning/critical alerts if predicted CPU exceeds a threshold

---

## Limitations

The current project is a successful proof-of-pipeline, but it has limitations.

### Current Limitations

- Only one week of telemetry was used.
- CPU usage was mostly low and stable.
- The project predicts CPU load, not a full server-health score.
- Container count stayed constant, so it did not add predictive variation.
- The model has not yet been tested on major overload, failure, or stress-test events.
- The current code is offline and not yet deployed as a live monitoring service.
- A future live version should save and reuse training scaler statistics for consistent inference.

---

## Future Work

Potential improvements include:

- collect several weeks or months of telemetry
- include high-load events such as Plex transcoding, backups, downloads, and simulated stress tests
- predict multiple targets, such as CPU, RAM, disk, and container CPU
- create a combined server-health score
- classify server state as normal, warning, or critical
- add anomaly detection
- deploy the trained model in a Docker container
- integrate predictions into Grafana
- create Prometheus-compatible prediction metrics
- add alerting based on predicted future load
- test model performance during real heavy server activity
---

## Final Presentation Summary

The final project presentation highlights:

- the smart media server monitoring problem
- the Prometheus data collection pipeline
- dataset size, structure, statistics, and visualizations
- preprocessing and target creation
- sliding-window generation
- MLP baseline model
- LSTM sequence model
- three experimental settings
- quantitative results using MSE, MAE, and RMSE
- actual-vs-predicted plots
- residual analysis
- limitations and future improvements

Main final result:

```text
The 30-minute LSTM had the best test RMSE: 0.0316
```

---

## References and Tools

- GitHub repository: `https://github.com/RyArnz/csc426-smart-media-ml-monitoring`
- TensorFlow/Keras: `https://www.tensorflow.org/`
- pandas: `https://pandas.pydata.org/`
- NumPy: `https://numpy.org/`
- matplotlib: `https://matplotlib.org/`
- Prometheus HTTP API: `https://prometheus.io/docs/prometheus/latest/querying/api/`

---
