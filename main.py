"""
Main Execution Pipeline for AIMLCZG523 MLOps Assignment 01.
Course: AIMLCZG523 - Machine Learning Operations (MLOps)
BITS ID: 2025AF05099

Orchestrates the entire machine learning lifecycle:
1. Data acquisition (download / verify)
2. Preprocessing & stratified split
3. Exploratory Data Analysis (EDA) visualizations
4. 3-Model training, hyperparameter tuning, & MLflow tracking
"""

import argparse
import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Set headless matplotlib config to prevent GUI/permission warnings
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

from src.data.download_data import download_dataset
from src.data.preprocess import split_and_save_data
from src.data.eda import generate_eda_plots
from src.models.train import train_and_evaluate


def print_banner():
    """Print project header banner."""
    print("=" * 65)
    print("  AIMLCZG523: MLOps Assignment 01 - Production ML Pipeline")
    print("  BITS ID: 2025AF05099")
    print("  Heart Disease Classifier: Cleveland Clinical Dataset")
    print("=" * 65)


def run_pipeline(stage: str = "all"):
    """Execute stages of the MLOps pipeline."""
    print_banner()

    # Stage 1: Data Acquisition
    if stage in ["all", "data"]:
        print("\n[Step 1/4] Checking UCI Heart Disease Dataset...")
        download_dataset()

    # Stage 2: Data Preprocessing & Splitting
    if stage in ["all", "data", "preprocess"]:
        print("\n[Step 2/4] Cleaning Data & Performing Stratified 80/20 Split...")
        split_and_save_data()

    # Stage 3: Exploratory Data Analysis Visualizations
    if stage in ["all", "eda"]:
        print("\n[Step 3/4] Generating Publication-Quality EDA Visualizations...")
        generate_eda_plots()

    # Stage 4: Model Training, Tuning, & MLflow Experiment Tracking
    if stage in ["all", "train"]:
        print("\n[Step 4/4] Training 3 Candidate Models & Logging to MLflow...")
        train_and_evaluate()

    print("\n" + "=" * 65)
    print(" [✓] Pipeline Stage Execution Completed Successfully!")
    print("=" * 65)


def main():
    parser = argparse.ArgumentParser(
        description="AIMLCZG523 MLOps Assignment 01 End-to-End ML Pipeline Runner"
    )
    parser.add_argument(
        "--stage",
        choices=["all", "data", "preprocess", "eda", "train"],
        default="all",
        help="Pipeline stage to execute (default: all)",
    )
    args = parser.parse_args()
    run_pipeline(stage=args.stage)


if __name__ == "__main__":
    main()

