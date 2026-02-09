# Customer Churn Predictor

## 📋 Overview

An end-to-end machine learning system designed to predict customer churn using the [Telco Customer Churn Dataset](https://www.kaggle.com/datasets/rashadrmammadov/customer-churn-dataset/data) from Kaggle. The project follows a complete MLOPs pipeline from exploratory data analysis to production deployment.

The project begins with comprehensive notebook-based experiments for EDA, data preprocessing, model training with hyperparameter tuning using Optuna, and model evaluation. These experiments are then converted into modular Python scripts implementing a robust data pipeline: data ingestion from MongoDB, preprocessing, model training, and evaluation with MLflow for experiment tracking.

The trained Logistic Regression model is served through a FastAPI backend with a `/predict` endpoint, providing real-time churn predictions. The entire API is containerised with Docker for consistent deployment.

A responsive React frontend with Tailwind CSS provides an intuitive interface for users to input customer data and receive churn predictions with probability scores. The frontend is also containerised for seamless deployment.

Finally, both containers are deployed on AWS infrastructure using Elastic Container Registry (ECR) for image storage and Elastic Container Service (ECS) with Fargate for serverless container orchestration, creating a fully cloud-deployed ML system.

## 🏗️ Architecture

![Architecture Diagram](churn-preditor-diagram.png)
![Frontend Image](frontend.png)

## 🛠️ Tech Stack

- **Frontend:** React, Tailwind
- **Backend:** FastAPI
- **ML:** Scikit-learn, Imblearn, Optuna, DVC, MLflow
- **Infrastructure:** Docker, AWS ECS, ECR
- **Data:** Pandas, NumPy, MongoDB

## 🚀 Features

- Real-time churn prediction via web interface
- RESTful API with automatic documentation
- Data pipeline with DVC
- Containerised deployment with Docker
- Cloud deployment on AWS ECS

## 📊 Model Performance

After hyperparameter tuning with Optuna, **Logistic Regression** performed best:

| Metric        | Score |
| ------------- | ----- |
| **Recall**    | 77%   |
| **Precision** | 53%   |
| **F1-Score**  | 63%   |
| **ROC-AUC**   | 0.853 |

### Prerequisites

- Python 3.8+
- Node.js 16+
- Docker
- MongoDB
