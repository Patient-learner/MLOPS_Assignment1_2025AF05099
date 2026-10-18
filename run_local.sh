#!/usr/bin/env bash
# ==============================================================================
# End-to-End Local Execution Script for AIMLCZG523 MLOps Assignment 01
# BITS ID: 2025AF05099
# ==============================================================================

set -e
export MPLCONFIGDIR="/tmp/matplotlib"

echo "=========================================================="
echo " Starting MLOps Pipeline Local Execution (AIMLCZG523)"
echo "=========================================================="

# 1. Environment Verification
if [ ! -d "venv" ]; then
    echo "[*] Creating Python 3.11 virtual environment..."
    python3.11 -m venv venv || python3 -m venv venv
    echo "[*] Installing dependencies..."
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt
fi

PYTHON="./venv/bin/python"

# 2. End-to-End ML Pipeline Execution
echo "[*] Executing end-to-end pipeline via main.py..."
$PYTHON main.py --stage all

# 3. Code Linting & Automated Unit Testing
echo "[*] Running Flake8 code linting..."
./venv/bin/flake8 src/ tests/ main.py --max-line-length=125 --ignore=E402,W503,E501,W391

echo "[*] Executing Pytest automated unit tests..."
./venv/bin/pytest -v tests/

echo "=========================================================="
echo " [✓] Local MLOps Foundation Pipeline Completed Successfully!"
echo "=========================================================="
echo "Next Steps:"
echo " 1. MLflow UI:        ./venv/bin/mlflow ui --port 5000"
echo " 2. Docker Run:       docker build -t heart-disease-api:v1 . && docker run -p 8000:8000 heart-disease-api:v1"
echo " 3. K8s Deploy:       minikube image load heart-disease-api:v1 && kubectl apply -f k8s/"
echo " 4. Monitoring Stack: docker compose -f monitoring/docker-compose.monitoring.yml up -d"
echo "=========================================================="
