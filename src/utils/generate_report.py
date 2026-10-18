"""
Automated Word Report (.docx) Generator for AIMLCZG523 MLOps Assignment 01.
Course: AIMLCZG523 - Machine Learning Operations (MLOps)
BITS ID: 2025AF05099

Calibrated to produce an exact 10-page academic submission in Microsoft Word.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FIGURES_DIR = os.path.join(BASE_DIR, "artifacts/figures")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "artifacts/screenshots")


def set_cell_background(cell, fill_hex: str):
    """Set background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)


def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
    """Set internal cell padding (dxa units)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)


def create_callout_box(doc, text: str, title: str = "KEY FINDING"):
    """Create a shaded callout box with a colored left accent border."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)

    tc_pr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="1F4E79"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tc_pr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r_title = p.add_run(f"📌 {title}: ")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(8.5)
    r_title.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    r_text = p.add_run(text)
    r_text.font.name = "Arial"
    r_text.font.size = Pt(8.5)


def embed_screenshot_figure(doc, img_rel_path: str, caption: str, width_in: float = 5.2):
    """Embed an actual screenshot with styled caption or fallback if missing."""
    img_full_path = os.path.join(SCREENSHOTS_DIR, img_rel_path)
    if os.path.exists(img_full_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(2)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture(img_full_path, width=Inches(width_in))

        p_cap = doc.add_paragraph(caption)
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].italic = True
        p_cap.runs[0].font.size = Pt(8.0)
        p_cap.paragraph_format.space_after = Pt(2)
    else:
        create_screenshot_placeholder(doc, 1, caption, "Screenshot file not found")


def create_screenshot_placeholder(doc, number: int, title: str, instructions: str, height_in: float = 2.0):
    """Create a designated screenshot container box for students to paste UI captures."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "FAFAFA")
    set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

    tc_pr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="dashed" w:sz="12" w:space="0" w:color="7F8C8D"/>'
        f'<w:left w:val="dashed" w:sz="12" w:space="0" w:color="7F8C8D"/>'
        f'<w:bottom w:val="dashed" w:sz="12" w:space="0" w:color="7F8C8D"/>'
        f'<w:right w:val="dashed" w:sz="12" w:space="0" w:color="7F8C8D"/>'
        f'</w:tcBorders>'
    )
    tc_pr.append(borders)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    r_title = p.add_run(f"📷 [SCREENSHOT {number}: {title.upper()}]\n")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(9)
    r_title.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)

    r_inst = p.add_run(f"Action: {instructions}\n(Paste image here)")
    r_inst.font.name = "Arial"
    r_inst.font.size = Pt(8)
    r_inst.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)
    r_inst.italic = True


def add_heading_with_spacing(doc, text: str, level: int):
    """Add a structured heading with uniform styling."""
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    if level == 1:
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)
        for r in h.runs:
            r.font.name = "Arial"
            r.font.size = Pt(13)
            r.bold = True
            r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    elif level == 2:
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
        for r in h.runs:
            r.font.name = "Arial"
            r.font.size = Pt(11)
            r.bold = True
            r.font.color.rgb = RGBColor(0x2E, 0x75, 0xB6)
    return h


def build_word_report(output_filename: str = "MLOps_Assignment1_Report_2025AF05099.docx"):
    """Compile comprehensive academic project report calibrated to exactly 10 pages."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_path = os.path.join(REPORTS_DIR, output_filename)

    doc = Document()

    # Configure Margins: 0.65 inches for calibrated 10-page layout
    for section in doc.sections:
        section.top_margin = Inches(0.65)
        section.bottom_margin = Inches(0.65)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)

    # =========================================================================
    # PAGE 1: TITLE, METADATA & SYSTEM ARCHITECTURE
    # =========================================================================
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_meta.add_run("BIRLA INSTITUTE OF TECHNOLOGY & SCIENCE, PILANI\n")
    r_uni.bold = True
    r_uni.font.name = "Arial"
    r_uni.font.size = Pt(12)
    r_uni.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    r_wilp = p_meta.add_run("Work Integrated Learning Programmes (WILP) | AIMLCZG523: MLOps Assignment 01\n")
    r_wilp.font.name = "Arial"
    r_wilp.font.size = Pt(10)
    r_wilp.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(8)
    r_main_title = p_title.add_run(
        "Production-Grade MLOps Pipeline: End-to-End Heart Disease Classifier\n"
        "CI/CD, MLflow Tracking, Docker Containerization & Kubernetes Deployment"
    )
    r_main_title.bold = True
    r_main_title.font.name = "Arial"
    r_main_title.font.size = Pt(14)
    r_main_title.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    # Metadata Summary Table
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_rows = [
        ("BITS ID", "2025AF05099"),
        ("Public GitHub Repository", "https://github.com/Patient-learner/MLOPS_Assignment1_2025AF05099"),
        ("Lab VM Execution Path", "/home/s2025af05099/workspace/MLOPS_Assignment1_2025AF05099"),
        ("Dataset", "UCI Heart Disease (Cleveland Clinical Repository - 13 Features + 1 Target)"),
        ("Serving Architecture", "FastAPI + Docker (Non-Root) + Minikube K8s + Prometheus + Grafana"),
        ("CI/CD Automation", "GitHub Actions (.github/workflows/ci.yml) with Automated Testing & Build"),
    ]
    for idx, (k, v) in enumerate(meta_rows):
        c0 = meta_table.cell(idx, 0)
        c1 = meta_table.cell(idx, 1)
        c0.text = k
        c1.text = v
        set_cell_background(c0, "F2F2F2")
        c0.paragraphs[0].runs[0].bold = True
        c0.paragraphs[0].runs[0].font.name = "Arial"
        c0.paragraphs[0].runs[0].font.size = Pt(8.5)
        c1.paragraphs[0].runs[0].font.name = "Arial"
        c1.paragraphs[0].runs[0].font.size = Pt(8.5)
        set_cell_margins(c0, 30, 30, 80, 80)
        set_cell_margins(c1, 30, 30, 80, 80)

    add_heading_with_spacing(doc, "1. Executive Summary & System Architecture", level=1)
    p = doc.add_paragraph(
        "This project uses the UCI Cleveland dataset to compare three classification models. "
        "Logistic regression achieved the highest cross-validation ROC-AUC, so its preprocessing and classifier were packaged together "
        "and served through FastAPI. The service was tested in Docker and deployed on Minikube. "
        "Pipeline reproducibility is ensured through fixed random seeds (seed=42), automated execution via main.py and run_local.sh, "
        "dependency version constraints in requirements.txt, and automated CI test verification on GitHub Actions."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)

    # Embed System Architecture Diagram
    arch_path = os.path.join(FIGURES_DIR, "system_architecture.png")
    if os.path.exists(arch_path):
        doc.add_picture(arch_path, width=Inches(4.9))
        p_cap = doc.add_paragraph("Figure 1: End-to-End MLOps System Architecture Diagram (Data, Modeling, Serving, Deployment & Monitoring)")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].italic = True
        p_cap.runs[0].font.size = Pt(8)

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: SETUP INSTRUCTIONS & DATA DICTIONARY
    # =========================================================================
    add_heading_with_spacing(doc, "2. Setup & Installation Instructions", level=1)
    p = doc.add_paragraph(
        "The repository is self-contained and reproducible across macOS, Linux, and Prayogshala lab VMs "
        "(deployed at /home/s2025af05099/workspace/MLOPS_Assignment1_2025AF05099). "
        "Because the repository is public, no authentication tokens are required for cloning."
    )
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(2)

    code_setup = (
        "# 1. Clone & Enter Directory: git clone https://github.com/Patient-learner/MLOPS_Assignment1_2025AF05099.git && cd MLOPS_Assignment1_2025AF05099\n"
        "# 2. Local Pipeline & Test Suite: chmod +x run_local.sh && ./run_local.sh\n"
        "# 3. Python Pipeline Stages: ./venv/bin/python main.py --stage all  (stages: data, preprocess, eda, train, report)\n"
        "# 4. Container Build: docker build -t heart-disease-api:v1 .\n"
        "# 5. Serving Option A (Compose): docker compose -f monitoring/docker-compose.monitoring.yml up -d  (API:8000, Grafana:3000)\n"
        "#    Serving Option B (K8s): minikube start && minikube image load heart-disease-api:v1 && kubectl apply -f k8s/\n"
        "#    Access K8s Service: kubectl port-forward svc/heart-disease-service 8080:8000"
    )
    p_code = doc.add_paragraph(code_setup)
    p_code.runs[0].font.name = "Courier New"
    p_code.runs[0].font.size = Pt(7.0)
    p_code.paragraph_format.line_spacing = 1.0
    p_code.paragraph_format.space_after = Pt(3)

    add_heading_with_spacing(doc, "3. Data Acquisition & Clinical Data Dictionary [Task 1]", level=1)
    p = doc.add_paragraph(
        "The UCI Heart Disease dataset comprises 303 patient records with 13 clinical input features and one binary target column collected from the Cleveland Clinic. "
        "Data ingestion is automated via src/data/download_data.py with local fallback caching for offline environments."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)

    # Features Description Table
    features_table = doc.add_table(rows=15, cols=4)
    features_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    f_headers = ["Attribute", "Clinical Description", "Measurement Range / Categories", "Pipeline Role"]
    for i, h in enumerate(f_headers):
        c = features_table.cell(0, i)
        c.text = h
        set_cell_background(c, "1F4E79")
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        c.paragraphs[0].runs[0].font.size = Pt(8)
        set_cell_margins(c, 30, 30, 50, 50)

    clinical_features = [
        ("age", "Patient age in years", "29 – 77 years", "Numeric (StandardScaler)"),
        ("sex", "Biological sex", "0 = Female, 1 = Male", "Binary (Mode Imputer)"),
        ("cp", "Chest pain type", "1 = Typical, 2 = Atypical, 3 = Non-anginal, 4 = Asymptomatic", "Categorical (OneHotEncoder)"),
        ("trestbps", "Resting blood pressure on hospital admission", "94 – 200 mm Hg", "Numeric (StandardScaler)"),
        ("chol", "Serum cholesterol", "126 – 564 mg/dl", "Numeric (StandardScaler)"),
        ("fbs", "Fasting blood sugar > 120 mg/dl", "0 = False, 1 = True", "Binary (Mode Imputer)"),
        ("restecg", "Resting ECG results", "0 = Normal, 1 = ST-T wave abnormality, 2 = LV hypertrophy", "Categorical (OneHotEncoder)"),
        ("thalach", "Maximum heart rate achieved during stress test", "71 – 202 bpm", "Numeric (StandardScaler)"),
        ("exang", "Exercise induced angina", "0 = No, 1 = Yes", "Binary (Mode Imputer)"),
        ("oldpeak", "ST depression induced by exercise relative to rest", "0.0 – 6.2 mm", "Numeric (StandardScaler)"),
        ("slope", "Slope of the peak exercise ST segment", "1 = Upsloping, 2 = Flat, 3 = Downsloping", "Categorical (OneHotEncoder)"),
        ("ca", "Number of major vessels (0-3) colored by fluoroscopy", "0, 1, 2, 3 vessels (4 missing in raw data)", "Categorical (Mode Imputer + OHE)"),
        ("thal", "Thallium heart scan defect", "3 = Normal, 6 = Fixed defect, 7 = Reversible defect", "Categorical (Mode Imputer + OHE)"),
        ("target", "Diagnosis of heart disease (angiographic disease status)", "0 = Absence (<50% diameter narrowing), 1 = Presence", "Target Variable (Binary)"),
    ]
    for idx, f_data in enumerate(clinical_features):
        for col_idx, val in enumerate(f_data):
            c = features_table.cell(idx + 1, col_idx)
            c.text = val
            c.paragraphs[0].runs[0].font.size = Pt(7.5)
            set_cell_margins(c, 25, 25, 40, 40)

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: EDA VISUALIZATIONS (4 FIGURES IN 2X2 GRID) & CLINICAL INSIGHTS
    # =========================================================================
    add_heading_with_spacing(doc, "3.1 Exploratory Data Analysis Visualizations", level=1)
    p = doc.add_paragraph(
        "Four EDA plots were generated to analyze class balance, feature distributions, feature correlations, "
        "and maximum heart rate distributions across patient age groups. The Cleveland dataset exhibits balanced target prevalence (54.1% Healthy, 45.9% Disease)."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)

    # 2x2 Grid of EDA Figures
    cb_path = os.path.join(FIGURES_DIR, "class_balance.png")
    hist_path = os.path.join(FIGURES_DIR, "feature_histograms.png")
    corr_path = os.path.join(FIGURES_DIR, "correlation_heatmap.png")
    scat_path = os.path.join(FIGURES_DIR, "age_vs_heart_rate.png")

    eda_table = doc.add_table(rows=2, cols=2)
    eda_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    if os.path.exists(cb_path):
        eda_table.cell(0, 0).paragraphs[0].add_run().add_picture(cb_path, width=Inches(2.9))
        p00 = eda_table.cell(0, 0).add_paragraph("Fig 2a: Target Class Balance")
        p00.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p00.runs[0].font.size = Pt(7.5)
        p00.runs[0].italic = True
    if os.path.exists(hist_path):
        eda_table.cell(0, 1).paragraphs[0].add_run().add_picture(hist_path, width=Inches(3.4))
        p01 = eda_table.cell(0, 1).add_paragraph("Fig 2b: Clinical Feature Distributions")
        p01.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p01.runs[0].font.size = Pt(7.5)
        p01.runs[0].italic = True
    if os.path.exists(corr_path):
        eda_table.cell(1, 0).paragraphs[0].add_run().add_picture(corr_path, width=Inches(3.1))
        p10 = eda_table.cell(1, 0).add_paragraph("Fig 2c: Correlation Heatmap")
        p10.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p10.runs[0].font.size = Pt(7.5)
        p10.runs[0].italic = True
    if os.path.exists(scat_path):
        eda_table.cell(1, 1).paragraphs[0].add_run().add_picture(scat_path, width=Inches(3.1))
        p11 = eda_table.cell(1, 1).add_paragraph("Fig 2d: Age vs Max Heart Rate")
        p11.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p11.runs[0].font.size = Pt(7.5)
        p11.runs[0].italic = True

    create_callout_box(
        doc,
        "Zero-Leakage & Clinical Insight: Imputation is performed inside the Scikit-Learn pipeline during 5-fold CV to prevent leakage. "
        "Maximum heart rate (thalach, r = -0.42) demonstrates strong protective correlation, while ST depression (oldpeak, r = +0.42) "
        "and fluoroscopy vessel blockage (ca, r = +0.46) represent the strongest risk indicators for heart disease.",
        "CLINICAL INSIGHTS & LEAK-FREE IMPUTATION"
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: FEATURE PIPELINE & 3-MODEL BENCHMARK COMPARISON
    # =========================================================================
    add_heading_with_spacing(doc, "4. Feature Engineering & 3-Model Benchmark [Tasks 2 & 3]", level=1)
    p = doc.add_paragraph(
        "A scikit-learn ColumnTransformer encapsulates data transformations inside the model pipeline: "
        "numerical features are standardized with StandardScaler, categorical features are one-hot encoded, and missing values "
        "are imputed with SimpleImputer. Three model families were benchmarked using 5-Fold Stratified Cross Validation with GridSearchCV:"
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)

    # Hyperparameter Grid Table
    hparam_table = doc.add_table(rows=4, cols=3)
    hparam_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_headers = ["Algorithm Family", "Hyperparameter Search Grid", "Selected Optimal Parameters"]
    for i, h in enumerate(h_headers):
        c = hparam_table.cell(0, i)
        c.text = h
        set_cell_background(c, "1F4E79")
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        c.paragraphs[0].runs[0].font.size = Pt(8)
        set_cell_margins(c, 40, 40, 50, 50)

    grid_info = [
        ("Logistic Regression (Generalized Linear)", "C: [0.01, 0.1, 1.0, 5.0, 10.0], penalty: ['l2'], solver: ['lbfgs', 'liblinear']", "C = 1.0, penalty = l2, solver = liblinear"),
        ("Random Forest (Bagging Ensemble)", "n_estimators: [50, 100, 150], max_depth: [3, 5, 8, None], min_samples_split: [2, 5]", "n_estimators = 50, max_depth = 8, min_samples_split = 2"),
        ("Gradient Boosting (Sequential Boosting)", "n_estimators: [50, 100, 150], learning_rate: [0.01, 0.05, 0.1], max_depth: [2, 3], subsample: [0.8, 1.0]", "n_estimators = 150, learning_rate = 0.01, max_depth = 3, subsample = 0.8"),
    ]
    for idx, g_data in enumerate(grid_info):
        for col_idx, val in enumerate(g_data):
            c = hparam_table.cell(idx + 1, col_idx)
            c.text = val
            c.paragraphs[0].runs[0].font.size = Pt(8)
            set_cell_margins(c, 30, 30, 50, 50)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(2)

    # Dynamic Model Comparison Table
    model_table = doc.add_table(rows=4, cols=6)
    model_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Model Architecture", "5-Fold CV ROC-AUC", "Test Accuracy", "Test Precision", "Test Recall", "Test ROC-AUC"]
    for i, h in enumerate(headers):
        c = model_table.cell(0, i)
        c.text = h
        set_cell_background(c, "1F4E79")
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        c.paragraphs[0].runs[0].font.size = Pt(8)
        set_cell_margins(c, 40, 40, 50, 50)

    rows_data = [
        ("Logistic Regression (Champion)", "0.9045", "88.52%", "83.87%", "92.86%", "0.9686"),
        ("Random Forest Classifier", "0.9006", "90.16%", "86.67%", "92.86%", "0.9481"),
        ("Gradient Boosting Classifier", "0.8860", "86.89%", "83.33%", "89.29%", "0.9481"),
    ]
    for row_idx, rdata in enumerate(rows_data):
        for col_idx, val in enumerate(rdata):
            c = model_table.cell(row_idx + 1, col_idx)
            c.text = val
            c.paragraphs[0].runs[0].font.size = Pt(8)
            set_cell_margins(c, 30, 30, 50, 50)
            if row_idx == 0:
                c.paragraphs[0].runs[0].bold = True
                set_cell_background(c, "EBF1F5")

    create_callout_box(
        doc,
        "Selection Rationale: Logistic Regression was selected strictly based on the highest 5-fold cross-validation score "
        "(CV ROC-AUC: 0.9045) with the test partition left completely untouched. On the held-out test split, "
        "the model identified 26 of 28 positive cases in the test set (92.86% recall), while maintaining 88.52% accuracy and 0.9686 test ROC-AUC.",
        "CHAMPION MODEL SELECTION RATIONALE"
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 5: ROC / CM PLOTS & MLFLOW TRACKING UI SCREENSHOT
    # =========================================================================
    add_heading_with_spacing(doc, "4.1 Champion Model Evaluation & MLflow Experiment Tracking", level=1)
    p = doc.add_paragraph(
        "Figure 3 displays the Confusion Matrix and ROC Curve for the champion Logistic Regression pipeline on the untouched test split (N=61). "
        "Out of 28 positive heart disease patients, the model correctly diagnoses 26, achieving a 92.86% clinical sensitivity rate."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)

    # Embed Champion ROC Curve & Confusion Matrix
    cm_path = os.path.join(FIGURES_DIR, "LogisticRegression_confusion_matrix.png")
    roc_path = os.path.join(FIGURES_DIR, "LogisticRegression_roc_curve.png")
    if os.path.exists(cm_path) and os.path.exists(roc_path):
        table_plots = doc.add_table(rows=1, cols=2)
        table_plots.alignment = WD_TABLE_ALIGNMENT.CENTER
        table_plots.cell(0, 0).paragraphs[0].add_run().add_picture(cm_path, width=Inches(2.7))
        table_plots.cell(0, 1).paragraphs[0].add_run().add_picture(roc_path, width=Inches(2.7))

        p_cap = doc.add_paragraph("Figure 3: Confusion Matrix (Left) and ROC Curve (Right) for Champion Logistic Regression Pipeline")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].italic = True
        p_cap.runs[0].font.size = Pt(8)

    p_mlflow = doc.add_paragraph(
        "MLflow Tracking: Experiment runs are structured under 'Heart_Disease_Prediction_AIMLCZG523' logging hyperparameters, "
        "5-fold CV ROC-AUC, test metrics (accuracy, precision, recall, F1, ROC-AUC), confusion matrix and ROC curve plots, and serialized pipeline models."
    )
    p_mlflow.paragraph_format.line_spacing = 1.15
    p_mlflow.paragraph_format.space_after = Pt(6)

    # MLflow Screenshot
    embed_screenshot_figure(
        doc,
        "MLFLOW.png",
        "Figure 4: MLflow Tracking Server UI showing 5-Fold CV hyperparameter tuning and model runs comparison",
        width_in=5.4
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 6: MODEL PACKAGING & FASTAPI SERVING
    # =========================================================================
    add_heading_with_spacing(doc, "5. Model Packaging & Inference REST API [Task 4]", level=1)
    p = doc.add_paragraph(
        "The champion model pipeline is serialized as models/model.joblib alongside structured schema metadata (models/model_metadata.json). "
        "A FastAPI prediction API was developed (src/api/app.py) providing strict Pydantic type validation for input data:"
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)

    p_api_desc = doc.add_paragraph(
        "• GET /health: Health probe endpoint returning HTTP 200 OK and model loaded status for Kubernetes liveness/readiness.\n"
        "• POST /predict: Inference endpoint consuming 13 clinical features in JSON format and returning binary prediction, clinical risk label, probability score, and model confidence.\n"
        "• GET /metrics: Prometheus-compatible telemetry endpoint exposing HTTP request counts, request latency histograms, and prediction distributions."
    )
    p_api_desc.paragraph_format.line_spacing = 1.15
    p_api_desc.paragraph_format.space_after = Pt(4)

    # FastAPI Swagger Screenshot
    embed_screenshot_figure(
        doc,
        "FastAPI_2.png",
        "Figure 5: FastAPI Swagger Documentation (/docs) demonstrating successful POST /predict execution and JSON response",
        width_in=5.2
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 7: CI/CD PIPELINE & AUTOMATED TESTING (12 UNIT TESTS)
    # =========================================================================
    add_heading_with_spacing(doc, "6. CI/CD Pipeline & Automated Testing [Task 5]", level=1)
    p = doc.add_paragraph(
        "A comprehensive automated testing suite consisting of 12 unit and integration tests was developed using Pytest. "
        "The test suite validates data ingestion integrity, missing value handling, model serialization consistency, clinical discrimination, "
        "and HTTP API status codes. The GitHub Actions workflow (.github/workflows/ci.yml) executes on every push and pull request."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)

    # Test Suite Table
    test_table = doc.add_table(rows=13, cols=3)
    test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_headers = ["Test Module", "Test Function Name", "Verification Target"]
    for i, h in enumerate(t_headers):
        c = test_table.cell(0, i)
        c.text = h
        set_cell_background(c, "1F4E79")
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        c.paragraphs[0].runs[0].font.size = Pt(8)
        set_cell_margins(c, 20, 20, 40, 40)

    test_cases = [
        ("tests/test_data.py", "test_raw_data_exists", "Confirms presence of UCI raw data"),
        ("tests/test_data.py", "test_data_cleaning_no_nulls", "Verifies zero NaN values after cleaning"),
        ("tests/test_data.py", "test_processed_splits_exist", "Ensures train.csv and test.csv exist with identical schemas"),
        ("tests/test_model.py", "test_model_file_exists", "Verifies models/model.joblib is created"),
        ("tests/test_model.py", "test_prediction_output_structure", "Validates keys in prediction dictionary"),
        ("tests/test_model.py", "test_clinical_risk_discrimination", "Verifies model assigns higher risk to pathological profile"),
        ("tests/test_model.py", "test_pipeline_handles_missing_values", "Verifies embedded SimpleImputer handles NaN features"),
        ("tests/test_api.py", "test_root_endpoint", "Checks landing page metadata and BITS ID: 2025AF05099"),
        ("tests/test_api.py", "test_health_endpoint", "Validates Kubernetes liveness probe returns status 200"),
        ("tests/test_api.py", "test_predict_endpoint_valid_healthy_payload", "Tests inference on healthy patient profile"),
        ("tests/test_api.py", "test_predict_endpoint_invalid_payload", "Asserts 422 Unprocessable Entity on out-of-range clinical inputs"),
        ("tests/test_api.py", "test_prometheus_metrics_endpoint", "Ensures Prometheus exposition format contains http_requests_total"),
    ]
    for idx, t_data in enumerate(test_cases):
        for col_idx, val in enumerate(t_data):
            c = test_table.cell(idx + 1, col_idx)
            c.text = val
            c.paragraphs[0].runs[0].font.size = Pt(7.0)
            set_cell_margins(c, 15, 15, 35, 35)

    # Pytest / Flake8 and GitHub CI Screenshots side by side
    sc_table = doc.add_table(rows=1, cols=2)
    sc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_ci1 = sc_table.cell(0, 0)
    c_ci2 = sc_table.cell(0, 1)

    pyt_path = os.path.join(SCREENSHOTS_DIR, "pytets_Flake8.png")
    gh_path = os.path.join(SCREENSHOTS_DIR, "Github_CI.png")

    if os.path.exists(pyt_path):
        p_c1 = c_ci1.paragraphs[0]
        p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c1.add_run().add_picture(pyt_path, width=Inches(2.85))
        p1_cap = c_ci1.add_paragraph("Figure 6: Automated verification showing clean Flake8 code linting and 12/12 passing Pytest unit tests")
        p1_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1_cap.runs[0].italic = True
        p1_cap.runs[0].font.size = Pt(7.0)

    if os.path.exists(gh_path):
        p_c2 = c_ci2.paragraphs[0]
        p_c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c2.add_run().add_picture(gh_path, width=Inches(2.85))
        p2_cap = c_ci2.add_paragraph("Figure 7: GitHub Actions CI automated pipeline green runs")
        p2_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2_cap.runs[0].italic = True
        p2_cap.runs[0].font.size = Pt(7.0)

    doc.add_page_break()

    # =========================================================================
    # PAGE 8: DOCKER CONTAINERIZATION & KUBERNETES DEPLOYMENT
    # =========================================================================
    add_heading_with_spacing(doc, "7. Docker Containerization & Kubernetes Deployment [Tasks 6 & 7]", level=1)
    p = doc.add_paragraph(
        "Containerization: A lightweight single-stage Dockerfile based on python:3.11-slim packages the application. "
        "The container executes under an unprivileged user (appuser, UID 1000) rather than root. "
        "A Docker HEALTHCHECK directive polls /health every 30 seconds to detect unhealthy container status."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)

    p_k8s = doc.add_paragraph(
        "Kubernetes Orchestration: Declarative manifests (k8s/deployment.yaml and k8s/service.yaml) deploy the application "
        "into a Minikube cluster. The deployment specifies CPU limits (500m), memory limits (512Mi), liveness probes (which restart failing pods), "
        "and readiness probes (which control traffic routing). The deployment was horizontally scaled across 4 healthy running pod replicas, "
        "with traffic routed through a LoadBalancer service exposing NodePort 30080."
    )
    p_k8s.paragraph_format.line_spacing = 1.15
    p_k8s.paragraph_format.space_after = Pt(4)

    # Kubernetes Scaled Pods Screenshot
    embed_screenshot_figure(
        doc,
        "kubernetes sacled pods & service.png",
        "Figure 8: Minikube Kubernetes cluster deployment showing 4 ready replica pods and LoadBalancer service exposing NodePort 30080",
        width_in=5.4
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 9: PRODUCTION MONITORING & GRAFANA DASHBOARD
    # =========================================================================
    add_heading_with_spacing(doc, "8. Production Monitoring & Observability [Task 8]", level=1)
    p = doc.add_paragraph(
        "Production observability is achieved via Prometheus metric scraping and an automated Grafana dashboard: "
        "Prometheus polls the /metrics endpoint every 5 seconds. Automated Grafana provisioning pre-configures Prometheus as a datasource "
        "and automatically imports the Heart Disease Production Dashboard upon container startup."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)

    # Telemetry Metrics Table
    telemetry_table = doc.add_table(rows=4, cols=3)
    telemetry_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    telem_headers = ["Prometheus Metric", "Metric Type", "Monitoring Purpose"]
    for i, h in enumerate(telem_headers):
        c = telemetry_table.cell(0, i)
        c.text = h
        set_cell_background(c, "1F4E79")
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        c.paragraphs[0].runs[0].font.size = Pt(8)
        set_cell_margins(c, 20, 20, 40, 40)

    telem_data = [
        ("http_requests_total", "Counter", "Tracks incoming HTTP traffic volume partitioned by method, endpoint, and status code (200, 422, 500)"),
        ("request_latency_seconds", "Histogram", "Tracks distribution of response times to evaluate 95th percentile latency SLAs (P95 < 50ms)"),
        ("heart_disease_predictions_total", "Counter", "Tracks output prediction distribution (positive vs negative inferences) to detect potential output distribution shifts"),
    ]
    for idx, row in enumerate(telem_data):
        for col_idx, val in enumerate(row):
            c = telemetry_table.cell(idx + 1, col_idx)
            c.text = val
            c.paragraphs[0].runs[0].font.size = Pt(7.5)
            set_cell_margins(c, 15, 15, 40, 40)

    # Grafana Screenshot
    embed_screenshot_figure(
        doc,
        "Grafana.png",
        "Figure 9: Live Grafana production dashboard monitoring Total Requests, Class Distributions, and P95 Latency",
        width_in=5.4
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 10: REFLECTION, VIDEO SCRIPT & SUBMISSION CHECKLIST
    # =========================================================================
    add_heading_with_spacing(doc, "9. Practical Engineering Reflection & Lessons Learned", level=1)
    p_refl = doc.add_paragraph()
    p_refl.paragraph_format.line_spacing = 1.05
    p_refl.paragraph_format.space_before = Pt(2)
    p_refl.paragraph_format.space_after = Pt(4)

    refl_points = [
        ("• In-Fold CV Imputation (Data Leakage Elimination): ",
         "Initially, missing values were imputed across the full training split before CV, subtly leaking validation statistics into training folds. Placing SimpleImputer directly inside the Scikit-learn Pipeline ensured imputation is fitted strictly inside each CV fold during GridSearchCV, maintaining rigorous separation between evaluation partitions."),
        ("• Grafana Telemetry Metric Label Alignment: ",
         "The initial Grafana dashboard queried an incorrect label name (numeric prediction_class), whereas the API was instrumented with prediction_label string values ('Heart Disease Present' / 'No Heart Disease'). Direct Prometheus API inspection revealed the mismatch, which was resolved by updating the PromQL expressions and verifying dashboard panels against live load."),
        ("• Prometheus Scrape Target Duplication: ",
         "Prometheus was initially configured with both 'heart-disease-api:8000' and 'host.docker.internal:8000'. Because both resolved to the same container, queries doubled request and prediction counts. Removing host.docker.internal restored exact 1:1 telemetry accuracy."),
        ("• Lightweight Container Hardening (Debian-Slim): ",
         "Transitioning from standard python:3.11 to python:3.11-slim and enforcing an unprivileged user (appuser, UID 1000) significantly decreased image footprint (down to ~450MB) and attack surface, ensuring compliant non-root execution across Kubernetes worker nodes."),
        ("• Automated CI Quality Gates: ",
         "Configuring GitHub Actions with automated Flake8 linting and Pytest regression suites prevented syntax anomalies and dependency breakages from entering the main branch, safeguarding the codebase against regressions prior to container image creation."),
    ]
    for b_title, b_desc in refl_points:
        r_bt = p_refl.add_run(b_title)
        r_bt.bold = True
        r_bt.font.name = "Arial"
        r_bt.font.size = Pt(8.5)
        r_bt.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
        r_bd = p_refl.add_run(b_desc + "\n")
        r_bd.font.name = "Arial"
        r_bd.font.size = Pt(8.5)

    add_heading_with_spacing(doc, "10. Production Roadmap & MLOps Recommendations", level=1)
    p_road = doc.add_paragraph(
        "Based on the empirical findings and production deployment of this pipeline, the following engineering enhancements "
        "are recommended for industrial-scale clinical operations:"
    )
    p_road.paragraph_format.line_spacing = 1.15
    p_road.paragraph_format.space_after = Pt(4)

    roadmap_items = [
        ("Automated Drift Monitoring & Retraining Triggers: ",
         "Deploy Evidently AI drift monitoring pipelines to compute Population Stability Index (PSI > 0.2 indicating significant distribution shift) and statistical tests on numerical features, triggering automated Airflow retraining DAGs upon confirmed feature drift."),
        ("Centralized Model Registry & Staging Gates: ",
         "Transition from file-based model artifacts to an enterprise MLflow Model Registry with staging, production, and archived lifecycle tags, enforced through automated cryptographic model signing and rollback mechanisms."),
        ("Canary Deployments & Shadow Scoring: ",
         "Implement service mesh routing for canary deployments (routing 5% of live traffic to challenger pods) and shadow scoring (duplicating production traffic to compare latency and model agreement without impacting client responses)."),
        ("Dataset Versioning with DVC: ",
         "Integrate Data Version Control (DVC) backed by object storage (S3/GCS) to track raw and processed dataset hashes alongside Git commits, reinforcing experimental reproducibility across model development iterations."),
    ]
    p_rm = doc.add_paragraph()
    p_rm.paragraph_format.line_spacing = 1.05
    p_rm.paragraph_format.space_after = Pt(4)
    for r_title, r_desc in roadmap_items:
        r_t = p_rm.add_run(f"• {r_title}")
        r_t.bold = True
        r_t.font.name = "Arial"
        r_t.font.size = Pt(8.5)
        r_t.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
        r_d = p_rm.add_run(r_desc + "\n")
        r_d.font.name = "Arial"
        r_d.font.size = Pt(8.5)

    # Save Document
    doc.save(report_path)
    print(f"[✓] Successfully compiled professional Word Report to: {report_path}")
    return report_path


if __name__ == "__main__":
    build_word_report()
