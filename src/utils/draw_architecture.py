"""
Generates a publication-quality architecture diagram for the MLOps Project Report.
Saves to artifacts/figures/system_architecture.png.
"""

import os
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

FIGURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../artifacts/figures"))


def generate_architecture_diagram(output_path: str = None):
    if output_path is None:
        os.makedirs(FIGURES_DIR, exist_ok=True)
        output_path = os.path.join(FIGURES_DIR, "system_architecture.png")

    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # Title
    ax.text(7, 7.6, "End-to-End MLOps System Architecture",
            ha="center", va="center", fontsize=18, fontweight="bold", color="#1a252f")
    ax.text(7, 7.2, "Course: AIMLCZG523 | BITS ID: 2025AF05099 | Heart Disease Classification Pipeline",
            ha="center", va="center", fontsize=11, color="#7f8c8d")

    # Stages definition: (x, y, width, height, title, items, color)
    boxes = [
        (0.5, 4.2, 2.8, 2.4, "1. Data Layer", [
            "UCI Cleveland Clinical Data",
            "13 Features + 1 Target",
            "Train-Imputed Mode (No Leak)",
            "Stratified 80/20 Train/Test Split"
        ], "#e8f4f8", "#2980b9"),

        (3.7, 4.2, 3.0, 2.4, "2. Pipeline & Modeling", [
            "ColumnTransformer (Impute+Scale+OHE)",
            "5-Fold Stratified Cross-Validation",
            "Models: LogisticReg, RF, GradBoost",
            "Champion: Logistic Reg (Recall: 92.9%)"
        ], "#eafaf1", "#27ae60"),

        (7.1, 4.2, 3.0, 2.4, "3. MLflow Tracking", [
            "Experiment: Heart_Disease_AIMLCZG523",
            "Logged Params, CV & Test Metrics",
            "Logged Artifacts: CM & ROC Plots",
            "Serialized: models/model.joblib"
        ], "#fef9e7", "#f39c12"),

        (10.5, 4.2, 3.0, 2.4, "4. FastAPI Serving", [
            "GET /health (Liveness/Readiness)",
            "POST /predict (Pydantic Schema)",
            "GET /metrics (Prometheus Exposer)",
            "Probability & Confidence Scoring"
        ], "#f4ecf7", "#8e44ad"),

        # Row 2 (Sequential Left to Right: 5 -> 6 -> 7)
        (0.5, 1.0, 3.8, 2.5, "5. CI/CD & Automated Testing", [
            "GitHub Actions CI (.github/workflows/ci.yml)",
            "Flake8 Linting + 12 Pytest Unit Tests",
            "Automated Model Training & Verification",
            "Artifact Upload & Docker Build Verification"
        ], "#ebf5fb", "#2980b9"),

        (4.7, 1.0, 4.2, 2.5, "6. Container & K8s Orchestration", [
            "Single-stage Dockerfile (python:3.11-slim)",
            "Secure Non-Root appuser Execution",
            "Minikube K8s Deployment (4 Scaled Pods)",
            "Service: LoadBalancer/NodePort :30080"
        ], "#eaeded", "#34495e"),

        (9.3, 1.0, 4.2, 2.5, "7. Monitoring & Observability", [
            "Prometheus Server (:9090) 5s Scrape",
            "Grafana Dashboard (:3000) Auto-Provisioned",
            "Real-time Latency (P95), QPS & Predictions",
            "Scrape Target: heart-disease-api:8000"
        ], "#fdedec", "#e74c3c"),
    ]

    for (x, y, w, h, title, items, bg_color, border_color) in boxes:
        # Card Background
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                                      facecolor=bg_color, edgecolor=border_color, linewidth=2)
        ax.add_patch(rect)

        # Card Header
        ax.text(x + w / 2, y + h - 0.25, title, ha="center", va="center",
                fontsize=11.5, fontweight="bold", color=border_color)

        # Card Content
        for idx, item in enumerate(items):
            ax.text(x + 0.15, y + h - 0.65 - (idx * 0.42), f"• {item}",
                    ha="left", va="center", fontsize=8.5, color="#2c3e50")

    # Connective Arrows between pipeline stages
    arrow_props = dict(facecolor="#34495e", edgecolor="#34495e", width=1.5, headwidth=7, headlength=7, shrink=0.05)

    # 1 -> 2
    ax.annotate("", xy=(3.7, 5.4), xytext=(3.3, 5.4), arrowprops=arrow_props)
    # 2 -> 3
    ax.annotate("", xy=(7.1, 5.4), xytext=(6.7, 5.4), arrowprops=arrow_props)
    # 3 -> 4
    ax.annotate("", xy=(10.5, 5.4), xytext=(10.1, 5.4), arrowprops=arrow_props)

    # 4 -> 5 (Code & Model Push to CI/CD via orthogonal channel)
    ax.plot([12.0, 12.0, 2.4, 2.4], [4.2, 3.85, 3.85, 3.55], color="#8e44ad", lw=2)
    ax.annotate("", xy=(2.4, 3.5), xytext=(2.4, 3.62),
                arrowprops=dict(facecolor="#8e44ad", edgecolor="#8e44ad", width=1.5, headwidth=7, headlength=7))
    ax.text(7.2, 3.85, "Git Push triggers Automated CI/CD", ha="center", va="center",
            fontsize=9.5, fontweight="bold", color="#8e44ad",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffffff", edgecolor="#8e44ad", lw=1.2))

    # 5 -> 6 (CI/CD to Container & K8s)
    ax.annotate("", xy=(4.7, 2.25), xytext=(4.3, 2.25), arrowprops=arrow_props)

    # 6 -> 7 (K8s to Monitoring)
    ax.annotate("", xy=(9.3, 2.25), xytext=(8.9, 2.25), arrowprops=arrow_props)

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"[✓] System Architecture Diagram generated: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_architecture_diagram()

