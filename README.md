# MLOps Assignment 01: End-to-End Heart Disease Classifier Pipeline
**Course:** AIMLCZG523 — Machine Learning Operations (MLOps)  
**BITS ID:** 2025AF05099  
**GitHub Repository:** [https://github.com/Patient-learner/MLOPS_Assignment1_2025AF05099](https://github.com/Patient-learner/MLOPS_Assignment1_2025AF05099)  
**Video Walkthrough:** [Watch Video Demonstration](https://github.com/Patient-learner/MLOPS_Assignment1_2025AF05099/blob/main/Video/MLOps_Assignment1_Video_Walkthrough_2025AF05099.mp4)  

---

## 1. Project Overview & Problem Statement
The objective of this assignment is to develop, package, deploy, and monitor an end-to-end, production-grade Machine Learning classification service predicting patient heart disease risk using the **UCI Heart Disease (Cleveland) Dataset**.

The solution follows modern MLOps engineering practices:
- **Reproducible Data Pipeline:** Automated acquisition, missing value imputation, and exploratory data analysis.
- **Model Development & Tuning:** Comparison of Linear (`LogisticRegression`) and Non-Linear Ensemble (`RandomForestClassifier`) models with 5-fold Stratified Cross-Validation.
- **Experiment Tracking:** Full parameter, metric, and plot logging with **MLflow**.
- **Model Packaging:** Complete Scikit-Learn `Pipeline` serialized via `joblib`.
- **API Serving:** High-performance REST API with **FastAPI** exposing `/predict`, `/health`, and Prometheus `/metrics`.
- **Containerization:** Lean, secure single-stage `Dockerfile` with non-root execution.
- **Orchestration:** Local Kubernetes deployment (`k8s/deployment.yaml`, `k8s/service.yaml`) demonstrating pod scaling and health probes.
- **Monitoring:** Prometheus metric scraping and Grafana dashboard visualization.
- **CI/CD:** Automated GitHub Actions pipeline verifying linting, unit tests, model reproducibility, and container build.

---

## 2. Architecture Workflow

```
[Raw UCI Data] ---> [Data Cleaning & EDA] ---> [MLflow Experiment Tracking]
                                                     |
                                            (Champion Model)
                                                     |
[Prometheus / Grafana] <--- [FastAPI Serving] <--- [Serialized Pipeline (.joblib)]
       ^                          ^
       |                          |
 [Scrape /metrics]        [Docker Container]
                                  ^
                                  |
                        [Kubernetes Pods & Svc]
```

---

## 3. Directory Structure
```text
MLOPS_Assignment1_2025AF05099/
├── .github/workflows/ci.yml       # GitHub Actions CI pipeline
├── data/
│   ├── raw/heart_disease.csv      # Downloaded raw Cleveland dataset
│   └── processed/                 # Cleaned dataset, train.csv, test.csv
├── notebooks/01_eda.ipynb         # Interactive Jupyter EDA notebook
├── src/
│   ├── data/
│   │   ├── download_data.py       # Data download script
│   │   ├── preprocess.py          # Preprocessing and train/test split
│   │   └── eda.py                 # Automated visualization plot generator
│   ├── models/
│   │   ├── train.py               # Model training, tuning & MLflow tracking
│   │   └── predict.py             # Inference engine
│   ├── api/
│   │   ├── app.py                 # FastAPI application
│   │   └── schemas.py             # Pydantic request/response schemas
│   └── utils/
│       └── logger.py              # Structured logging utility
├── tests/
│   ├── test_data.py               # Data schema & missing value tests
│   ├── test_model.py              # Model prediction & discrimination tests
│   └── test_api.py                # API integration & metrics tests
├── k8s/
│   ├── deployment.yaml            # K8s Deployment with health probes
│   └── service.yaml               # K8s Service (LoadBalancer/NodePort)
├── monitoring/
│   ├── prometheus.yml             # Prometheus scrape configuration
│   └── docker-compose.monitoring.yml # Local Prometheus + Grafana stack
├── artifacts/figures/             # EDA and model performance plots
├── models/                        # Serialized model and metadata
├── Dockerfile                     # Container definition
├── main.py                        # Python end-to-end pipeline orchestrator
├── requirements.txt               # Pinned dependencies
└── run_local.sh                   # One-command bootstrap and test runner
```

---

## 4. Quick Start (Local Run)

### 4.1 Automated Setup (Recommended)
Run the end-to-end local bootstrap, pipeline, and test runner:
```bash
chmod +x run_local.sh
./run_local.sh
```

### 4.2 Python Pipeline Runner (`main.py`)
Alternatively, if your environment is already active:
```bash
# Run all stages (Data -> Preprocessing -> EDA -> Train -> Report)
python main.py

# Or run specific stages
python main.py --stage data
python main.py --stage train
python main.py --stage report
```

### 4.3 Manual Step-by-Step Execution

#### Step 1: Environment Setup
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 2: Data Acquisition & EDA
```bash
python src/data/download_data.py
python src/data/preprocess.py
python src/data/eda.py
```
*Visualizations are generated in `artifacts/figures/` (`class_balance.png`, `correlation_heatmap.png`, `feature_histograms.png`, `age_vs_heart_rate.png`).*

#### Step 3: Model Training & MLflow Experiment Tracking
```bash
python src/models/train.py
```
*To inspect the MLflow UI:*
```bash
mlflow ui --port 5000
```
Open [http://localhost:5000](http://localhost:5000) to view runs, metrics, parameters, and logged artifacts.

#### Step 4: Run Automated Unit Tests & Linting
```bash
flake8 src/ tests/ main.py --max-line-length=125 --ignore=E402,W503,E501,W391
pytest -v tests/
```

#### Step 5: Build and Run Docker Serving Container
```bash
# Build Docker image
docker build -t heart-disease-api:v1 .

# Run container locally
docker run -d --name heart-disease-api -p 8000:8000 heart-disease-api:v1

# Test Health Endpoint
curl http://localhost:8000/health

# Test Predict Endpoint (Sample Healthy Patient)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45, "sex": 0, "cp": 1, "trestbps": 120.0, "chol": 190.0,
    "fbs": 0, "restecg": 0, "thalach": 175.0, "exang": 0,
    "oldpeak": 0.0, "slope": 1, "ca": 0.0, "thal": 3.0
  }'

# Test Metrics Endpoint
curl http://localhost:8000/metrics

# Stop and remove standalone container to free port 8000 and container name
docker stop heart-disease-api && docker rm heart-disease-api
```

#### Step 6: Deploy to Local Kubernetes
```bash
# Start Minikube cluster
minikube start --driver=docker

# Load local Docker image into Minikube node
minikube image load heart-disease-api:v1

# Apply manifests
kubectl apply -f k8s/

# Verify Pods & Service
kubectl get pods -l app=heart-disease-api
kubectl get svc heart-disease-service

# Demonstrate Pod Scaling (4 replicas)
kubectl scale deployment heart-disease-api --replicas=4
kubectl get pods -l app=heart-disease-api

# Access Service locally via port 8080 (avoids port 8000 conflicts):
kubectl port-forward svc/heart-disease-service 8080:8000
# Test in a separate terminal:
curl http://localhost:8080/health
# Alternatively on Linux/Prayogshala: minikube service heart-disease-service --url
```

#### Step 7: Launch Monitoring Stack (Prometheus + Grafana)
```bash
# Launch full stack (API, Prometheus, Grafana) via Docker Compose
docker compose -f monitoring/docker-compose.monitoring.yml up -d
```
- **Prometheus UI:** [http://localhost:9090](http://localhost:9090) (Scrapes `/metrics` every 5 seconds)
- **Grafana UI:** [http://localhost:3000](http://localhost:3000) *(User: `admin` / Password: `admin`)*
- *Note: Grafana is pre-provisioned with Prometheus as the default datasource and automatically loads the 'Heart Disease Classifier Production Dashboard' upon startup.*

To shut down the monitoring stack:
```bash
docker compose -f monitoring/docker-compose.monitoring.yml down
```

---

## 5. Model Performance Comparison

| Model Architecture | 5-Fold CV ROC-AUC | Test Accuracy | Test Precision | Test Recall | Test F1-Score | Test ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Champion)** | **0.9045** | **88.52%** | **83.87%** | **92.86%** | **0.8814** | **0.9686** |
| Random Forest Classifier | 0.8997 | 85.25% | 85.19% | 82.14% | 0.8364 | 0.9416 |
| Gradient Boosting Classifier | 0.8870 | 86.89% | 83.33% | 89.29% | 0.8621 | 0.9491 |

The regularized `LogisticRegression` pipeline achieved the highest 5-fold Cross-Validation ROC-AUC (0.9045) and highest test ROC-AUC (0.9686) with 92.86% clinical recall, making it optimal for clinical risk prediction where minimizing dangerous False Negatives is paramount. The evaluation demonstrates rigorous comparison across three distinct machine learning paradigms: Generalized Linear, Bagging Ensemble, and Sequential Boosting.


