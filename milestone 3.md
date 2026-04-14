Milestone 3: Deep Learning Model Development & Training
Project Title: AI-Driven Monitoring and Predictive Maintenance for a Smart Home Media Server

Overview
The goal of Milestone 3 was to design, implement, and train deep learning models for a practical server-monitoring task using real telemetry from a smart home media server. For this milestone, the project focused on multivariate time-series forecasting rather than classification. The model uses recent server behavior to predict near-future CPU load, which creates a strong foundation for future predictive maintenance features such as overload warnings, anomaly detection, and maintenance-risk classification. 
Prediction Task
The forecasting task was defined as follows:
    • Input: the previous 60 minutes of server telemetry 
    • Output: the next 10-minute average CPU usage 
This setup was chosen because CPU load is one of the most important indicators of system stress in a media server environment, especially when containers and background services are active. Forecasting future CPU behavior makes the system more useful than simply reacting to current usage because it allows earlier warning and future expansion into predictive maintenance logic. 
Data Collection
The dataset was collected from Prometheus using the Prometheus HTTP API. Metrics were pulled from the server over the period from April 7, 2026 to April 14, 2026 using a 60-second step interval. The export produced a dataset with 10,081 rows and the following columns:
    • timestamp 
    • server_cpu_percent 
    • server_ram_percent 
    • disk_usage_percent 
    • container_ram_mb 
    • container_cpu_cores 
    • container_count 
The Prometheus queries successfully returned data for each selected metric, and the final exported CSV contained no missing values across any of the collected fields.
Preprocessing
The raw Prometheus export was converted into a training-ready time-series dataset through several preprocessing steps. First, timestamps were parsed and sorted in chronological order. The feature names were then standardized into cleaner names used by the training pipeline. After that, the data was prepared for forecasting by creating a target column representing the future 10-minute average CPU usage.
The dataset was split by time order, not by random shuffling, to preserve the integrity of the forecasting task and prevent leakage from future observations into the training set. The resulting split sizes were:
    • Training rows: 7,051 
    • Validation rows: 1,510 
    • Test rows: 1,510 
Feature scaling was fit using training-set statistics only, which ensured that information from validation and test data did not leak into the training process.
Windowing
After preprocessing, the data was transformed into equal-length supervised time-series windows. Each sample used a window size of 60 time steps, representing the previous 60 minutes of telemetry, to predict one future target value.
The final supervised dataset shapes were:
    • X_train: (6991, 60, 6) 
    • X_val: (1450, 60, 6) 
    • X_test: (1450, 60, 6) 
This confirm that the data pipeline successfully converted the Prometheus telemetry into a format suitable for both a baseline neural model and a sequence-aware recurrent model.
Model Development
Two TensorFlow/Keras models were implemented and compared.
Baseline Model: MLP
The baseline model was a multilayer perceptron (MLP) that flattened each 60-step time window into a single vector before passing it through dense layers. Its architecture was:
    • Flatten 
    • Dense(64, ReLU) 
    • Dense(32, ReLU) 
    • Dense(1) 
The MLP contained 25,217 trainable parameters. It served as a simple neural baseline that could learn general relationships between recent telemetry and future CPU load, but it did not explicitly model sequential dependencies in time. 
Primary Model: LSTM
The primary model was an LSTM designed specifically for time-series forecasting. Its architecture was:
    • LSTM(64) 
    • Dropout(0.2) 
    • Dense(16, ReLU) 
    • Dense(1) 
The LSTM contained 19,233 trainable parameters. Unlike the MLP, it was designed to capture temporal structure across the 60-step input sequence, making it a better fit for forecasting server behavior over time. 
Training Configuration
Both models were compiled with:
    • Loss function: Mean Squared Error (MSE) 
    • Metric: Mean Absolute Error (MAE) 
Training used validation monitoring and model checkpointing through the pipeline. TensorFlow ran on CPU because CUDA drivers were not available on my laptop, so no GPU acceleration was used. Despite that, both models trained and evaluated successfully. 
Results
Most Recent Comparable Training Run
The most recent side-by-side training run produced the following test results:
Model	Test MSE	Test MAE	Test RMSE
MLP	0.0032	0.0440	0.0561
LSTM	0.0021	0.0367	0.0453
In this run, the LSTM outperformed the MLP on every evaluation metric. This indicates that the sequential model was better able to learn patterns in the telemetry data and produce more accurate short-term CPU forecasts. 
Best Saved Evaluation Run
A saved LSTM evaluation run also produced even stronger results:
    • MSE: 0.0016 
    • MAE: 0.0317 
    • RMSE: 0.0402 
The best saved LSTM checkpoint provided the strongest overall forecasting performance observed during the project’s current milestone stage. 
Interpretation
The results show that the telemetry collected from the media server contains meaningful information that can be used to forecast future CPU behavior. The baseline MLP provided a useful comparison point, but the LSTM consistently performed better because it is designed to capture sequential dependencies across time.
This result is important because server performance is not purely static. CPU usage is influenced by patterns that happen over time, such as rising container activity, sustained system load, or periods of heavier disk and memory usage. By modeling sequences directly, the LSTM was better able to anticipate future CPU behavior than the flattened MLP baseline.
Overall, the LSTM’s stronger performance supports the use of recurrent deep learning for short-horizon server forecasting in this project.
Deliverables Completed
By the end of Milestone 3, the project successfully produced:
    • a working Prometheus-based telemetry collection pipeline 
    • a cleaned and processed time-series dataset 
    • time-ordered train, validation, and test splits 
    • supervised window generation for deep learning input 
    • a baseline MLP forecasting model 
    • a primary LSTM forecasting model 
    • saved training artifacts and checkpoints 
    • evaluation metrics 
    • predicted-vs-actual outputs 
    • residual analysis outputs 
    • learning-curve and evaluation plots 
These deliverables demonstrate that the full deep learning workflow is functioning end-to-end.
Conclusion
Milestone 3 was successfully completed by collecting real Prometheus telemetry from the smart home media server, transforming it into supervised time-series windows, and training two deep learning models for CPU forecasting. The LSTM outperformed the baseline MLP on all evaluation metrics, showing sequence-aware modeling improves short-term CPU prediction in this environment. This milestone establishes a strong technical foundation for the next stage of the project, where forecasting outputs can be extended into predictive maintenance alerts, anomaly detection, or classification-based risk labels. 
References
    • Github Repo: https://github.com/RyArnz/csc426-smart-media-ml-monitoring
