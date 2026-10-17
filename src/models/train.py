"""
Model training, hyperparameter tuning, and MLflow experiment tracking.
Compares Logistic Regression and Random Forest Classifier on UCI Heart Disease dataset.
Saves the champion model pipeline to models/model.joblib for production serving.
"""

import os
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import mlflow
import mlflow.sklearn

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/processed"))
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../models"))
FIGURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../artifacts/figures"))

# Define feature sets (ca is vessel count 0-3, treated as categorical/discrete)
NUMERIC_FEATURES = ["age", "trestbps", "chol", "thalach", "oldpeak"]
CATEGORICAL_FEATURES = ["cp", "restecg", "slope", "thal", "ca"]
BINARY_FEATURES = ["sex", "fbs", "exang"]


def get_preprocessor() -> ColumnTransformer:
    """Create reproducible scikit-learn preprocessing pipeline with embedded imputation."""
    num_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    cat_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    bin_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
    ])

    return ColumnTransformer(
        transformers=[
            ("num", num_transformer, NUMERIC_FEATURES),
            ("cat", cat_transformer, CATEGORICAL_FEATURES),
            ("bin", bin_transformer, BINARY_FEATURES),
        ]
    )


def save_confusion_matrix_plot(y_true, y_pred, model_name: str, output_path: str):
    """Plot and save confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    ax.set(
        xticks=np.arange(cm.shape[1]),
        yticks=np.arange(cm.shape[0]),
        xticklabels=["No Disease (0)", "Disease (1)"],
        yticklabels=["No Disease (0)", "Disease (1)"],
        title=f"Confusion Matrix - {model_name}",
        ylabel="True Diagnosis",
        xlabel="Predicted Diagnosis",
    )
    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(
                j,
                i,
                format(cm[i, j], "d"),
                ha="center",
                va="center",
                color="white" if cm[i, j] > thresh else "black",
                fontweight="bold",
                fontsize=13,
            )
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def save_roc_curve_plot(y_true, y_prob, model_name: str, roc_auc: float, output_path: str):
    """Plot and save ROC curve."""
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, color="#2980b9", lw=2.5, label=f"ROC curve (AUC = {roc_auc:.3f})")
    plt.plot([0, 1], [0, 1], color="#7f8c8d", lw=1.5, linestyle="--", label="Random Classifier")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate (1 - Specificity)")
    plt.ylabel("True Positive Rate (Sensitivity)")
    plt.title(f"ROC Curve - {model_name}", fontweight="bold")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def train_and_evaluate():
    """Execute end-to-end model training, hyperparameter tuning, and MLflow logging."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    # 1. Load Train and Test Data
    train_df = pd.read_csv(os.path.join(DATA_DIR, "train.csv"))
    test_df = pd.read_csv(os.path.join(DATA_DIR, "test.csv"))

    X_train = train_df.drop(columns=["target"])
    y_train = train_df["target"]
    X_test = test_df.drop(columns=["target"])
    y_test = test_df["target"]

    print(f"[*] Training samples: {len(X_train)}, Testing samples: {len(X_test)}")

    # 2. Setup MLflow Experiment
    tracking_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../mlruns"))
    mlflow.set_tracking_uri(f"file://{tracking_dir}")
    experiment_name = "Heart_Disease_Prediction_AIMLCZG523"
    mlflow.set_experiment(experiment_name)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # Models to compare
    models_config = {
        "LogisticRegression": {
            "pipeline": Pipeline([
                ("preprocessor", get_preprocessor()),
                ("classifier", LogisticRegression(random_state=42, max_iter=1000)),
            ]),
            "param_grid": {
                "classifier__C": [0.01, 0.1, 1.0, 5.0, 10.0],
                "classifier__penalty": ["l2"],
                "classifier__solver": ["lbfgs", "liblinear"],
            },
        },
        "RandomForestClassifier": {
            "pipeline": Pipeline([
                ("preprocessor", get_preprocessor()),
                ("classifier", RandomForestClassifier(random_state=42)),
            ]),
            "param_grid": {
                "classifier__n_estimators": [50, 100, 150],
                "classifier__max_depth": [3, 5, 8, None],
                "classifier__min_samples_split": [2, 5],
            },
        },
        "GradientBoostingClassifier": {
            "pipeline": Pipeline([
                ("preprocessor", get_preprocessor()),
                ("classifier", GradientBoostingClassifier(random_state=42)),
            ]),
            "param_grid": {
                "classifier__n_estimators": [50, 100, 150],
                "classifier__learning_rate": [0.01, 0.05, 0.1],
                "classifier__max_depth": [2, 3],
                "classifier__subsample": [0.8, 1.0],
            },
        },
    }

    best_cv_score = -1.0
    champion_model_pipeline = None
    champion_model_name = ""
    champion_metrics = {}
    all_models_summary = {}

    for model_name, config in models_config.items():
        with mlflow.start_run(run_name=f"Run_{model_name}"):
            print("\n==================================================")
            print(f"[*] Training and tuning: {model_name}")
            grid = GridSearchCV(
                estimator=config["pipeline"],
                param_grid=config["param_grid"],
                cv=cv,
                scoring="roc_auc",
                n_jobs=1,
                refit=True,
            )
            grid.fit(X_train, y_train)

            best_model = grid.best_estimator_
            best_params = grid.best_params_
            cv_roc_auc = grid.best_score_

            # Test Set Evaluation
            y_pred = best_model.predict(X_test)
            y_prob = best_model.predict_proba(X_test)[:, 1]

            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)
            rec = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_prob)

            print(f"[+] Best Params: {best_params}")
            print(f"[+] 5-Fold CV ROC-AUC: {cv_roc_auc:.4f}")
            print(f"[+] Test Accuracy:     {acc:.4f}")
            print(f"[+] Test Precision:    {prec:.4f}")
            print(f"[+] Test Recall:       {rec:.4f}")
            print(f"[+] Test F1-Score:     {f1:.4f}")
            print(f"[+] Test ROC-AUC:      {roc_auc:.4f}")

            # Record model summary
            all_models_summary[model_name] = {
                "best_params": best_params,
                "cv_roc_auc": round(float(cv_roc_auc), 4),
                "test_accuracy": round(float(acc), 4),
                "test_precision": round(float(prec), 4),
                "test_recall": round(float(rec), 4),
                "test_f1": round(float(f1), 4),
                "test_roc_auc": round(float(roc_auc), 4),
            }

            # MLflow Logging
            mlflow.log_params(best_params)
            mlflow.log_metrics({
                "cv_roc_auc": cv_roc_auc,
                "test_accuracy": acc,
                "test_precision": prec,
                "test_recall": rec,
                "test_f1": f1,
                "test_roc_auc": roc_auc,
            })

            # Save and log artifacts
            cm_plot_path = os.path.join(FIGURES_DIR, f"{model_name}_confusion_matrix.png")
            roc_plot_path = os.path.join(FIGURES_DIR, f"{model_name}_roc_curve.png")
            save_confusion_matrix_plot(y_test, y_pred, model_name, cm_plot_path)
            save_roc_curve_plot(y_test, y_prob, model_name, roc_auc, roc_plot_path)

            mlflow.log_artifact(cm_plot_path)
            mlflow.log_artifact(roc_plot_path)
            mlflow.sklearn.log_model(best_model, artifact_path="model")

            # Select champion model based strictly on 5-Fold CV ROC-AUC (zero test-leakage)
            if cv_roc_auc > best_cv_score:
                best_cv_score = cv_roc_auc
                champion_model_pipeline = best_model
                champion_model_name = model_name
                champion_metrics = {
                    "cv_roc_auc": round(float(cv_roc_auc), 4),
                    "accuracy": round(float(acc), 4),
                    "precision": round(float(prec), 4),
                    "recall": round(float(rec), 4),
                    "f1": round(float(f1), 4),
                    "roc_auc": round(float(roc_auc), 4),
                    "params": best_params,
                }

    # 3. Save Champion Model for Production
    model_save_path = os.path.join(MODELS_DIR, "model.joblib")
    metadata_save_path = os.path.join(MODELS_DIR, "model_metadata.json")

    joblib.dump(champion_model_pipeline, model_save_path)

    import json
    metadata = {
        "champion_model": champion_model_name,
        "selection_metric": "5-fold Stratified CV ROC-AUC",
        "champion_cv_score": round(float(best_cv_score), 4),
        "metrics": champion_metrics,
        "all_models_summary": all_models_summary,
        "param_grids": {k: v["param_grid"] for k, v in models_config.items()},
        "features": {
            "numeric": NUMERIC_FEATURES,
            "categorical": CATEGORICAL_FEATURES,
            "binary": BINARY_FEATURES,
        },
    }
    with open(metadata_save_path, "w") as f:
        json.dump(metadata, f, indent=4)

    print("\n==================================================")
    print(f"[✓] Champion Model Selected: {champion_model_name} (CV ROC-AUC: {best_cv_score:.4f}, Test ROC-AUC: {champion_metrics['roc_auc']:.4f})")
    print(f"[✓] Serialized Model Pipeline saved to: {model_save_path}")
    print(f"[✓] Model Metadata saved to: {metadata_save_path}")
    print("==================================================")


if __name__ == "__main__":
    train_and_evaluate()
