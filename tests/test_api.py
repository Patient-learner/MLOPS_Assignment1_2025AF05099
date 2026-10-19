"""
Integration tests for FastAPI endpoints (/health, /predict, /metrics).
"""

from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)


def test_root_endpoint():
    """Verify landing page endpoint returns 200 and docs links."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "documentation" in data
    assert data["bits_id"] == "2025AF05099"
    assert data["author_id"] == "2025AF05099"


def test_health_endpoint():
    """Verify health probe returns status 200 and healthy flag."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


def test_predict_endpoint_valid_healthy_payload():
    """Verify prediction endpoint with a healthy patient profile."""
    payload = {
        "age": 42,
        "sex": 0,
        "cp": 1,
        "trestbps": 120.0,
        "chol": 195.0,
        "fbs": 0,
        "restecg": 0,
        "thalach": 172.0,
        "exang": 0,
        "oldpeak": 0.0,
        "slope": 1,
        "ca": 0.0,
        "thal": 3.0,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "label" in data
    assert "probability" in data
    assert "confidence" in data
    assert data["prediction"] in [0, 1]


def test_predict_endpoint_invalid_payload():
    """Verify malformed or out-of-range input triggers a 422 error."""
    # Invalid age (199 > 120) and negative blood pressure
    invalid_payload = {
        "age": 199,
        "sex": 1,
        "cp": 2,
        "trestbps": -10.0,
        "chol": 200.0,
        "fbs": 0,
        "restecg": 0,
        "thalach": 150.0,
        "exang": 0,
        "oldpeak": 1.0,
        "slope": 1,
        "ca": 0.0,
        "thal": 3.0,
    }
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422

    # Invalid fractional vessel count ca=1.5 must trigger 422
    ca_invalid_payload = {
        "age": 55, "sex": 1, "cp": 2, "trestbps": 130.0, "chol": 220.0,
        "fbs": 0, "restecg": 0, "thalach": 150.0, "exang": 0,
        "oldpeak": 1.0, "slope": 1, "ca": 1.5, "thal": 3.0,
    }
    assert client.post("/predict", json=ca_invalid_payload).status_code == 422

    # Invalid thallium category thal=999 must trigger 422
    thal_invalid_payload = {
        "age": 55, "sex": 1, "cp": 2, "trestbps": 130.0, "chol": 220.0,
        "fbs": 0, "restecg": 0, "thalach": 150.0, "exang": 0,
        "oldpeak": 1.0, "slope": 1, "ca": 0.0, "thal": 999.0,
    }
    res = client.post("/predict", json=thal_invalid_payload)
    assert res.status_code == 422


def test_prometheus_metrics_endpoint():
    """Verify Prometheus metrics are exposed and populated."""
    # First make a prediction to increment metric counters
    payload = {
        "age": 58,
        "sex": 1,
        "cp": 3,
        "trestbps": 135.0,
        "chol": 240.0,
        "fbs": 0,
        "restecg": 1,
        "thalach": 155.0,
        "exang": 0,
        "oldpeak": 1.2,
        "slope": 2,
        "ca": 1.0,
        "thal": 3.0,
    }
    client.post("/predict", json=payload)

    # Scrape metrics
    metrics_response = client.get("/metrics")
    assert metrics_response.status_code == 200
    metrics_text = metrics_response.text

    assert "http_requests_total" in metrics_text
    assert "heart_disease_predictions_total" in metrics_text
    assert "request_latency_seconds" in metrics_text
