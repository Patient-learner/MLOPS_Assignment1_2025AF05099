"""
Exploratory Data Analysis (EDA) module for UCI Heart Disease Dataset.
Generates publication-quality visualizations for assignment reports and documentation.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

RAW_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/raw/heart_disease.csv"))
FIGURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../artifacts/figures"))

# Configure matplotlib style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"font.size": 11, "figure.autolayout": True})


def generate_eda_plots(data_path: str = RAW_DATA_PATH, output_dir: str = FIGURES_DIR) -> dict[str, str]:
    """Generate and save all essential EDA visualizations."""
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(data_path)

    # Impute for visual consistency
    df["ca"] = df["ca"].fillna(df["ca"].mode()[0])
    df["thal"] = df["thal"].fillna(df["thal"].mode()[0])

    saved_plots = {}

    # 1. Class Balance Plot
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = df["target"].value_counts().sort_index()
    labels = ["0: No Disease", "1: Heart Disease"]
    colors = ["#2ecc71", "#e74c3c"]
    bars = ax.bar(labels, counts.values, color=colors, edgecolor="black", width=0.55)
    for bar in bars:
        yval = bar.get_height()
        pct = (yval / len(df)) * 100
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            yval + 3,
            f"{yval} ({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontweight="bold",
        )
    ax.set_title("UCI Heart Disease - Class Balance (Target Distribution)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Patient Count")
    ax.set_ylim(0, max(counts.values) + 25)
    plot1_path = os.path.join(output_dir, "class_balance.png")
    plt.savefig(plot1_path, dpi=300)
    plt.close()
    saved_plots["class_balance"] = plot1_path

    # 2. Histograms of Continuous Clinical Features
    num_features = ["age", "trestbps", "chol", "thalach", "oldpeak"]
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()
    for idx, feat in enumerate(num_features):
        sns.histplot(
            data=df,
            x=feat,
            hue="target",
            kde=True,
            palette={0: "#2ecc71", 1: "#e74c3c"},
            ax=axes[idx],
            element="step",
        )
        axes[idx].set_title(f"Distribution of {feat.upper()}", fontweight="bold")
        axes[idx].set_xlabel(feat)
    # Hide unused 6th subplot
    axes[5].axis("off")
    fig.suptitle("Histograms of Continuous Clinical Features Stratified by Diagnosis", fontsize=15, fontweight="bold")
    plot2_path = os.path.join(output_dir, "feature_histograms.png")
    plt.savefig(plot2_path, dpi=300)
    plt.close()
    saved_plots["feature_histograms"] = plot2_path

    # 3. Correlation Heatmap
    fig, ax = plt.subplots(figsize=(11, 9))
    corr_matrix = df.corr()
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        ax=ax,
        cbar_kws={"shrink": 0.8},
    )
    ax.set_title("Correlation Heatmap of UCI Heart Disease Features", fontsize=14, fontweight="bold")
    plot3_path = os.path.join(output_dir, "correlation_heatmap.png")
    plt.savefig(plot3_path, dpi=300)
    plt.close()
    saved_plots["correlation_heatmap"] = plot3_path

    # 4. Age vs Max Heart Rate (thalach) with Target hue
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(
        data=df,
        x="age",
        y="thalach",
        hue="target",
        palette={0: "#2ecc71", 1: "#e74c3c"},
        style="target",
        s=70,
        alpha=0.85,
        ax=ax,
    )
    ax.set_title("Age vs. Maximum Heart Rate (thalach) by Disease Status", fontsize=13, fontweight="bold")
    ax.set_xlabel("Age (years)")
    ax.set_ylabel("Max Heart Rate Achieved (thalach)")
    handles, _ = ax.get_legend_handles_labels()
    ax.legend(handles, ["No Disease", "Heart Disease"], title="Diagnosis")
    plot4_path = os.path.join(output_dir, "age_vs_heart_rate.png")
    plt.savefig(plot4_path, dpi=300)
    plt.close()
    saved_plots["age_vs_heart_rate"] = plot4_path

    print(f"[+] Successfully generated {len(saved_plots)} EDA plots in: {output_dir}")
    for name, path in saved_plots.items():
        print(f"    - {name}: {path}")

    return saved_plots


if __name__ == "__main__":
    generate_eda_plots()
