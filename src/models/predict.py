"""
Model inference module.
Loads the serialized champion model pipeline and performs predictions with confidence scores.
"""

import os
import joblib
import pandas as pd
from typing import Any, Dict, Union

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../models/model.joblib"))


class HeartDiseasePredictor:
    """Inference engine for Heart Disease prediction."""

    def __init__(self, model_path: str = MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Champion model binary not found at: {model_path}. Run train.py first.")
        self.model = joblib.load(model_path)
        self.feature_columns = [
            "age", "sex", "cp", "trestbps", "chol", "fbs",
            "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"
        ]

    def predict(self, input_data: Union[Dict[str, Any], pd.DataFrame]) -> Dict[str, Any]:
        """
        Accepts patient health feature dictionary or DataFrame and returns
        prediction class, human-readable label, and confidence score.
        """
        if isinstance(input_data, dict):
            df = pd.DataFrame([input_data])
        else:
            df = input_data.copy()

        # Ensure required columns exist
        missing_cols = [col for col in self.feature_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Input missing required features: {missing_cols}")

        df = df[self.feature_columns]

        # Predict class and probabilities
        pred_class = int(self.model.predict(df)[0])
        prob = float(self.model.predict_proba(df)[0][1])

        confidence = prob if pred_class == 1 else (1.0 - prob)
        label = "Heart Disease Present" if pred_class == 1 else "No Heart Disease"

        return {
            "prediction": pred_class,
            "label": label,
            "probability": round(prob, 4),
            "confidence": round(confidence, 4),
        }


if __name__ == "__main__":
    predictor = HeartDiseasePredictor()
    # Sample negative patient case (Healthy)
    sample_healthy = {
        "age": 45, "sex": 0, "cp": 1, "trestbps": 120, "chol": 190,
        "fbs": 0, "restecg": 0, "thalach": 175, "exang": 0,
        "oldpeak": 0.0, "slope": 1, "ca": 0, "thal": 3
    }
    # Sample positive patient case (High Risk)
    sample_risk = {
        "age": 67, "sex": 1, "cp": 4, "trestbps": 160, "chol": 286,
        "fbs": 0, "restecg": 2, "thalach": 108, "exang": 1,
        "oldpeak": 2.6, "slope": 2, "ca": 3, "thal": 7
    }

    print("Healthy Patient Prediction:", predictor.predict(sample_healthy))
    print("High Risk Patient Prediction:", predictor.predict(sample_risk))

