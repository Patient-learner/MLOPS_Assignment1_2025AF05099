"""
Pydantic schemas for request validation and response formatting.
"""

from pydantic import BaseModel, Field


class PatientData(BaseModel):
    age: int = Field(..., ge=1, le=120, description="Age in years (e.g. 58)")
    sex: int = Field(..., ge=0, le=1, description="Sex (1 = male; 0 = female)")
    cp: int = Field(..., ge=1, le=4, description="Chest pain type (1, 2, 3, or 4)")
    trestbps: float = Field(..., ge=50, le=250, description="Resting blood pressure in mm Hg")
    chol: float = Field(..., ge=50, le=600, description="Serum cholesterol in mg/dl")
    fbs: int = Field(..., ge=0, le=1, description="Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)")
    restecg: int = Field(..., ge=0, le=2, description="Resting electrocardiographic results (0, 1, 2)")
    thalach: float = Field(..., ge=40, le=250, description="Maximum heart rate achieved")
    exang: int = Field(..., ge=0, le=1, description="Exercise induced angina (1 = yes; 0 = no)")
    oldpeak: float = Field(..., ge=0.0, le=10.0, description="ST depression induced by exercise")
    slope: int = Field(..., ge=1, le=3, description="Slope of the peak exercise ST segment (1, 2, 3)")
    ca: float = Field(..., ge=0.0, le=3.0, description="Number of major vessels colored by flourosopy (0-3)")
    thal: float = Field(..., description="Thalassemia (3 = normal; 6 = fixed defect; 7 = reversable defect)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 63,
                "sex": 1,
                "cp": 3,
                "trestbps": 145.0,
                "chol": 233.0,
                "fbs": 1,
                "restecg": 0,
                "thalach": 150.0,
                "exang": 0,
                "oldpeak": 2.3,
                "slope": 2,
                "ca": 0.0,
                "thal": 3.0,
            }
        }
    }


class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="0 = No Disease, 1 = Heart Disease")
    label: str = Field(..., description="Clinical interpretation label")
    probability: float = Field(..., description="Model estimated probability of heart disease [0, 1]")
    confidence: float = Field(..., description="Confidence score of classification")
    model_version: str = Field(default="1.0.0", description="Serving model version")


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str
    app_name: str

