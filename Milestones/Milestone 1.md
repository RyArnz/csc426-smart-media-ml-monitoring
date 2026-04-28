# Milestone 1 (10%): Project Initiation and Planning

**Project Title:** AI-Driven Monitoring and Predictive Maintenance for a Smart Home Media Server  
**Team Members:** Ryan Arnzen, Prasiddha Neupane  
**Date:** February 15, 2026  

---

## Problem Description and Motivation

Modern self-hosted media servers operate continuously and run multiple Docker-based services (e.g., media streaming, cloud storage, reverse proxies, and download automation). Over time, system performance may degrade due to high CPU load, increasing memory usage, disk pressure, background downloads, or inefficient media transcoding.

Manual monitoring is inconsistent and reactive. This project aims to design and implement a machine learning system that monitors server performance metrics and predicts potential overload or maintenance needs before failures occur. By applying supervised learning methods, the system will provide predictive insights and support automated nightly maintenance decisions when necessary.

---

## Type of Machine Learning Task

The primary task will be **supervised learning using regression**. A linear neural network (or linear regression model) will be trained to predict future system performance metrics such as:

- CPU usage  
- Memory utilization  
- Disk growth  

Based on predicted values, the system will determine whether maintenance actions should be triggered.

---

## Initial Project Plan

- **Week 1:** Finalize project scope, define target variable, and set up metric collection from the server.
- **Week 2:** Perform exploratory data analysis and feature engineering (rolling averages, lag features).
- **Week 3:** Implement baseline linear regression model and evaluate using MSE/MAE..
- **Week 4:** Integrate model into nightly maintenance decision script.
- **Final Week:** Testing, documentation, and preparation of final report and demonstration.

---

## Team Member Responsibilities

**Ryan Arnzen**
- Server architecture integration  
- Data collection pipeline  
- Feature engineering  
- Model implementation (regression baseline)  
- Automation and nightly maintenance integration  

**Prasiddha Neupane**
- Exploratory data analysis  
- Model evaluation and comparison  
- Performance analysis and visualization  
- Documentation and final report preparation  

Both team members will collaborate on model tuning, testing, and presentation preparation.

---

## Communication Strategy

Project coordination and progress tracking will be managed through GitHub (Issues, Projects, and commit history). Regular communication will occur through text or discord for quick collaboration and discussion. Long discussion will be held in person or over teams.
