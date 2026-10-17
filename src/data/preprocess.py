"""
Preprocessing pipeline for UCI Heart Disease dataset.
Handles missing value imputation, type validation, and train-test splitting.
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split

RAW_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/raw/heart_disease.csv"))
PROCESSED_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/processed"))


def load_and_clean_data(raw_path: str = RAW_DATA_PATH) -> pd.DataFrame:
    """Load raw dataset and apply basic cleaning without test leakage."""
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw data file not found at: {raw_path}")

    df = pd.read_csv(raw_path)

    # Mode imputation for standalone clean view (ca and thal)
    if "ca" in df.columns:
        df["ca"] = df["ca"].fillna(df["ca"].mode()[0])
    if "thal" in df.columns:
        df["thal"] = df["thal"].fillna(df["thal"].mode()[0])

    int_cols = [
        "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
        "thalach", "exang", "slope", "ca", "thal", "target"
    ]
    for col in int_cols:
        if col in df.columns:
            df[col] = df[col].astype(int)

    return df


def split_and_save_data(test_size: float = 0.2, random_state: int = 42) -> tuple[str, str]:
    """
    Split raw dataset into stratified train and test sets.
    Retains raw missing values in train.csv and test.csv so that the Scikit-Learn
    pipeline's SimpleImputer performs imputation strictly inside each cross-validation fold,
    eliminating all statistical leakage across folds.
    Also produces heart_disease_cleaned.csv for exploratory analysis.
    """
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    raw_df = pd.read_csv(RAW_DATA_PATH)

    # 1. Save cleaned version for exploratory data analysis
    cleaned_df = load_and_clean_data(RAW_DATA_PATH)
    cleaned_path = os.path.join(PROCESSED_DATA_DIR, "heart_disease_cleaned.csv")
    cleaned_df.to_csv(cleaned_path, index=False)

    # 2. Stratified split directly on raw data without pre-imputation
    train_df, test_df = train_test_split(
        raw_df,
        test_size=test_size,
        random_state=random_state,
        stratify=raw_df["target"],
    )

    train_path = os.path.join(PROCESSED_DATA_DIR, "train.csv")
    test_path = os.path.join(PROCESSED_DATA_DIR, "test.csv")

    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    print(f"[+] Cleaned dataset (for EDA) saved to: {cleaned_path}")
    print(f"[+] Train dataset ({len(train_df)} rows) saved to: {train_path} (Raw missing values preserved for in-fold CV imputation)")
    print(f"[+] Test dataset ({len(test_df)} rows) saved to: {test_path} (Held-out unbiased evaluation)")

    return train_path, test_path


if __name__ == "__main__":
    split_and_save_data()
