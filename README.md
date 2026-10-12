# MedSafe — ML-Based Medication Safety Assistant

MedSafe is an interactive educational prototype designed to help users identify medication scenarios requiring clinical review. It combines deterministic reference-based safety checks with a Machine Learning risk priority classifier.

## Core Features
- **Duplicate Ingredient Detection**: Identifies overlapping active ingredients across different brand products.
- **Drug Interaction Verification**: Flags known interactions against verified reference pairs.
- **Missing Information Warnings**: Alerts users to incomplete drug profile entries.
- **ML Review Priority Classifier**: Uses a Random Forest classifier trained on synthetic scenario data to assign review priorities (Low, Moderate, High).

## Directory Structure
```
MedSafe/
├── app.py
├── train_model.py
├── medication_checks.py
├── generate_dataset.py
├── requirements.txt
├── README.md
├── data/
│   └── synthetic_medications.csv
├── models/
│   └── risk_model.joblib
└── tests/
    └── test_medication_checks.py
```

## Installation & Setup

1. **Unzip the project**:
   ```bash
   unzip MedSafe.zip
   cd MedSafe
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate synthetic dataset & train model**:
   ```bash
   python train_model.py
   ```

4. **Run unit tests**:
   ```bash
   pytest tests/
   ```

5. **Launch Streamlit Dashboard**:
   ```bash
   streamlit run app.py
   ```

## Disclaimer
MedSafe is a research and educational prototype. It is not intended to diagnose diseases, prescribe treatments, or substitute for professional clinical judgment.
