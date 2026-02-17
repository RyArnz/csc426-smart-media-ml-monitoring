# CSC 426 Deep Learning – Smart Media Server ML Monitoring

This project applies supervised learning to home media server metrics to:
1) predict future system load (regression), and/or
2) classify abnormal behavior or maintenance needs (classification),
then trigger a safe nightly maintenance workflow when needed.

## Problem
Home media servers run 24/7 and can degrade over time due to disk pressure,
background downloads, transcoding spikes, or runaway containers. Manual
monitoring is inconsistent.

## Task Type
- Regression: predict a numerical target such as CPU%, RAM%, disk growth, or a maintenance score.
- Classification: predict a discrete label such as normal/abnormal or maintenance-needed.

## Data
Metrics/log features may include:
- CPU%, RAM%, disk usage%, I/O, network throughput
- container counts, docker stats
- request counts (e.g., streaming sessions), transcoding indicators

## Model Plan
Baseline model: linear regression / linear neural network.
Evaluation: train/validation/test split (do not use test data during model building).

## Automation
A nightly job runs and:
- generates features from the last 24h window
- makes a prediction
- runs maintenance actions only if required
- saves a report in a file

## Tech Exploration (Media Server Context)
Usenet, Eweka/EZ News providers, HEVC/H.265, Overseerr, and reverse proxy tradeoffs (Nginx vs Apache).
