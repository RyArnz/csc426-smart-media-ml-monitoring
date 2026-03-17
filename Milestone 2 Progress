Milestone 2 — Data Collection and Preprocessing
Overview

Milestone 2 focuses on collecting, understanding, and preparing monitoring data from the home media server so it can be used for machine learning experiments.
To accomplish this, a monitoring stack was deployed using Prometheus, Node Exporter, cAdvisor, and Grafana. These tools collect system telemetry from the server and Docker containers and store it as time-series metrics.

The goal of this milestone was to:
Build a reliable data collection pipeline
Understand the structure of the monitoring data
Identify useful features for machine learning
Create an initial dataset export workflow
This milestone establishes the foundation needed for later deep learning and anomaly detection models.

System Monitoring Architecture
The monitoring system collects data from multiple layers of the server.
Server Hardware
      │
      ▼
Node Exporter
(host metrics)
      │
      ▼
cAdvisor
(container metrics)
      │
      ▼
Prometheus
(time-series database)
      │
      ▼
Grafana
(data visualization + analysis)

Node Exporter
Node Exporter collects host-level metrics including:
CPU utilization
RAM usage
Disk usage
Network activity
System load

These metrics describe the overall health of the server.
cAdvisor
cAdvisor monitors Docker containers and provides metrics such as:
Container CPU usage
Container memory usage
Container network usage
Number of running containers
This allows the system to understand how individual applications affect system performance.

Prometheus
Prometheus acts as the central monitoring database.
It performs:
periodic scraping of exporter metrics
time-series storage
query processing through PromQL
Prometheus provides the dataset that will later be used for machine learning training.

Grafana
Grafana is used to visualize the collected data and verify that monitoring is functioning correctly.
Dashboards were created to observe:
system resource usage
container resource consumption
storage usage
application-level performance
Grafana helped confirm that the collected data is accurate and stable before exporting it for ML use.
Dataset Description

The dataset consists of time-series server telemetry.
Each row represents the state of the server at a specific timestamp.

Example dataset structure:
timestamp	server_cpu_percent	server_ram_percent	disk_usage_percent	container_ram_mb	container_cpu	container_count
2026-03-16 19:00	1.3	12.6	19.6	1200	0.25	10
2026-03-16 19:01	1.4	12.7	19.6	1210	0.30	10

Features Collected
The following metrics were identified as useful features for the machine learning model.
Server metrics
Feature	Description	Unit
server_cpu_percent	Overall CPU utilization	%
server_ram_percent	Memory usage	%
disk_usage_percent	Root filesystem usage	%
Container metrics
Feature	Description	Unit
container_ram_mb	Total memory used by containers	MB
container_cpu	Total CPU usage of containers	CPU cores
container_count	Number of running containers	count
Application-level metrics (examples)

Individual containers can also be monitored.
Examples include:
Plex CPU usage
Plex RAM usage
Nextcloud CPU usage
Nextcloud RAM usage
MariaDB memory usage
These metrics allow the model to detect which service is causing resource spikes.

Data Collection Method
Metrics are collected by Prometheus at regular intervals.
Typical scrape interval:
30 seconds
The data is stored in the Prometheus time-series database and can be accessed through the Prometheus HTTP API.

Example query used to calculate disk usage:
(node_filesystem_size_bytes{fstype!="tmpfs",mountpoint="/"}
 - node_filesystem_free_bytes{fstype!="tmpfs",mountpoint="/"}) / node_filesystem_size_bytes{fstype!="tmpfs",mountpoint="/"}

Data Export Workflow
To prepare the dataset for machine learning training, Prometheus data will be exported through the API and converted into a structured dataset.

Workflow:
Prometheus
      │
      ▼
PromQL query
      │
      ▼
Prometheus HTTP API
      │
      ▼
Python export script
      │
      ▼
CSV dataset
      │
      ▼
Machine Learning pipeline

The exported dataset will then be used for:
preprocessing
normalization
model training
anomaly detection
Preprocessing Plan
Before training machine learning models, the dataset must be prepared.

Planned preprocessing steps include:
1. Timestamp alignment
All metrics will be aligned to consistent time intervals.
2. Handling missing values
Missing values may occur when:
containers restart
exporters temporarily fail
These will be handled using:
interpolation
forward filling
removal of corrupted rows

3. Feature scaling
Metrics will be normalized using techniques such as:
Min-Max scaling
standardization
This ensures neural networks train correctly.

4. Feature selection
Not all metrics are equally useful.
The model will focus on features most related to system stress:
CPU utilization
memory usage
container activity
disk pressure

Project Workflow
The full project pipeline currently looks like this:
Server Metrics
     │
     ▼
Prometheus Monitoring
     │
     ▼
Grafana Visualization
     │
     ▼
Dataset Export (Python)
     │
     ▼
Data Preprocessing
     │
     ▼
Machine Learning Model
     │
     ▼
Anomaly Detection / Predictive Maintenance

Key Technologies
Technology	Purpose
Docker	containerized applications
Prometheus	monitoring database
Node Exporter	host telemetry
cAdvisor	container telemetry
Grafana	monitoring dashboards
Python	dataset export and ML pipeline
