"""
Trains a Random Forest classifier to categorize medication scenarios into review priorities.
Evaluates model performance and exports the trained pipeline.
"""
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from generate_dataset import generate_synthetic_data


def train_and_evaluate():
    data_path = "data/synthetic_medications.csv"
    if not os.path.exists(data_path):
        df = generate_synthetic_data()
        os.makedirs("data", exist_ok=True)
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)

    X = df[[
        "num_medications",
        "has_duplicate_ingredient",
        "has_interaction",
        "has_missing_info",
        "patient_age",
        "total_daily_doses"
    ]]
    y = df["review_priority"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    print("=== Classification Report ===")
    print(classification_report(y_pred, y_test, target_names=["Low Risk", "Moderate Risk", "High Risk"]))

    print("\n=== Confusion Matrix ===")
    print(confusion_matrix(y_test, y_pred))

    os.makedirs("models", exist_ok=True)
    model_path = "models/risk_model.joblib"
    joblib.dump(clf, model_path)
    print(f"\nModel saved successfully to '{model_path}'.")


if __name__ == "__main__":
    train_and_evaluate()
