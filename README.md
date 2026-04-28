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
