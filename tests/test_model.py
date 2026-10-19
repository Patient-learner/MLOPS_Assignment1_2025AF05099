"""
Unit tests for model pipeline loading, inference consistency,
and output validation.
"""

import os
import pytest
from src.models.predict import HeartDiseasePredictor

MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../models/model.joblib")
)


@pytest.fixture(scope="module")
def predictor():
    """Fixture providing initialized predictor instance."""
    return HeartDiseasePredictor(model_path=MODEL_PATH)


def test_model_file_exists():
    """Verify serialized champion model exists."""
    assert os.path.exists(MODEL_PATH), f"Model not found at {MODEL_PATH}"


def test_prediction_output_structure(predictor):
    """Verify inference returns all required fields with proper types."""
    sample = {
        "age": 55, "sex": 1, "cp": 2, "trestbps": 130, "chol": 220,
        "fbs": 0, "restecg": 1, "thalach": 160, "exang": 0,
        "oldpeak": 1.0, "slope": 2, "ca": 0, "thal": 3
    }
    result = predictor.predict(sample)

    assert "prediction" in result
    assert "label" in result
    assert "probability" in result
    assert "confidence" in result

    assert result["prediction"] in [0, 1]
    assert 0.0 <= result["probability"] <= 1.0
    assert 0.5 <= result["confidence"] <= 1.0


def test_clinical_risk_discrimination(predictor):
    """Verify high-risk cardiac profile yields higher risk than healthy."""
    healthy_patient = {
        "age": 35, "sex": 0, "cp": 1, "trestbps": 110, "chol": 170,
        "fbs": 0, "restecg": 0, "thalach": 180, "exang": 0,
        "oldpeak": 0.0, "slope": 1, "ca": 0, "thal": 3
    }
    high_risk_patient = {
        "age": 68, "sex": 1, "cp": 4, "trestbps": 165, "chol": 290,
        "fbs": 1, "restecg": 2, "thalach": 105, "exang": 1,
        "oldpeak": 3.0, "slope": 2, "ca": 3, "thal": 7
    }

    healthy_res = predictor.predict(healthy_patient)
    risk_res = predictor.predict(high_risk_patient)

    assert risk_res["probability"] > healthy_res["probability"]
    assert healthy_res["prediction"] == 0
    assert risk_res["prediction"] == 1


def test_pipeline_handles_missing_values(predictor):
    """Verify pipeline SimpleImputer predicts even when features are NaN."""
    import numpy as np
    patient_with_missing_values = {
        "age": 52, "sex": 1, "cp": 2, "trestbps": 128, "chol": 205,
        "fbs": 0, "restecg": 1, "thalach": 155, "exang": 0,
        "oldpeak": 0.5, "slope": 2, "ca": np.nan, "thal": np.nan
    }
    result = predictor.predict(patient_with_missing_values)
    assert result["prediction"] in [0, 1]
    assert 0.0 <= result["probability"] <= 1.0
