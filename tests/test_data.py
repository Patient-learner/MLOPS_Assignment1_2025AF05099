"""
Unit tests for data acquisition and preprocessing.
"""

import os
import pandas as pd
from src.data.preprocess import load_and_clean_data

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))


def test_raw_data_exists():
    """Verify raw dataset file exists."""
    raw_path = os.path.join(DATA_DIR, "raw/heart_disease.csv")
    assert os.path.exists(raw_path), f"Raw data missing at {raw_path}"


def test_data_cleaning_no_nulls():
    """Verify cleaned dataset has zero missing values."""
    df = load_and_clean_data()
    assert df.isnull().sum().sum() == 0, "Cleaned dataset contains NaN values"
    assert len(df.columns) == 14, "Cleaned dataset does not have 14 columns"


def test_processed_splits_exist():
    """Verify train and test splits exist and have consistent features."""
    train_path = os.path.join(DATA_DIR, "processed/train.csv")
    test_path = os.path.join(DATA_DIR, "processed/test.csv")

    assert os.path.exists(train_path), "train.csv does not exist"
    assert os.path.exists(test_path), "test.csv does not exist"

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    assert set(train_df.columns) == set(test_df.columns)
    assert "target" in train_df.columns
    assert len(train_df) > len(test_df)
