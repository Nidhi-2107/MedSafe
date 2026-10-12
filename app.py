"""
Streamlit interactive web dashboard for MedSafe.
"""
import os
import joblib
import pandas as pd
import streamlit as st
from medication_checks import (
    check_duplicate_ingredients,
    check_missing_info,
    check_drug_interactions
)

st.set_page_config(
    page_title="MedSafe - Medication Safety Assistant",
    page_icon="💊",
    layout="wide"
)

# Load ML Model
MODEL_PATH = "models/risk_model.joblib"


@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


model = load_model()

st.title("💊 MedSafe — ML-Based Medication Safety Assistant")
st.caption("A decision-support prototype identifying safety flags, duplicate ingredients, and interaction risks.")

st.sidebar.header("📋 Patient Profile")
patient_age = st.sidebar.number_input("Patient Age", min_value=1, max_value=120, value=65)

st.subheader("Medication Scenario Entry")

default_meds = [
    {"name": "Tylenol Extra Strength", "ingredients": "Acetaminophen", "dosage": "500mg"},
    {"name": "Excedrin PM", "ingredients": "Acetaminophen, Diphenhydramine", "dosage": "250mg"}
]

if "med_list" not in st.session_state:
    st.session_state.med_list = default_meds

num_meds = st.number_input("Number of medications to evaluate", min_value=1, max_value=10, value=len(st.session_state.med_list))

current_meds = []
for i in range(int(num_meds)):
    col1, col2, col3 = st.columns([3, 4, 3])
    default_name = st.session_state.med_list[i]["name"] if i < len(st.session_state.med_list) else ""
    default_ing = st.session_state.med_list[i]["ingredients"] if i < len(st.session_state.med_list) else ""
    default_dos = st.session_state.med_list[i]["dosage"] if i < len(st.session_state.med_list) else ""

    with col1:
        med_name = st.text_input(f"Medication #{i+1} Name", value=default_name, key=f"name_{i}")
    with col2:
        ing_str = st.text_input(f"Active Ingredient(s) (comma-separated)", value=default_ing, key=f"ing_{i}")
    with col3:
        dosage = st.text_input(f"Dosage", value=default_dos, key=f"dos_{i}")

    ingredients_list = [x.strip() for x in ing_str.split(",") if x.strip()]
    current_meds.append({
        "name": med_name,
        "ingredients": ingredients_list,
        "dosage": dosage
    })

st.markdown("---")

if st.button("Run Safety Evaluation", type="primary"):
    # Deterministic Rule Checks
    duplicates = check_duplicate_ingredients(current_meds)
    missing_info = check_missing_info(current_meds)
    interactions = check_drug_interactions(current_meds)

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("🔍 Verified Safety Rule Flags")

        if duplicates:
            for dup in duplicates:
                st.error(f"⚠️ **{dup['message']}**")
        else:
            st.success("✅ No duplicate active ingredients detected.")

        if interactions:
            for inter in interactions:
                st.warning(f"⚡ **Interaction Flag ({inter['severity']} Severity):**\n"
                           f"Between {', '.join(inter['drugs'])}: {inter['description']}")
        else:
            st.success("✅ No verified reference interactions detected.")

        if missing_info:
            for miss in missing_info:
                st.info(f"ℹ️ **Incomplete Record:** {miss}")

    with col_right:
        st.subheader("🤖 ML Review Priority Classifier")

        if model is None:
            st.warning("ML Model artifact not found. Please run `python train_model.py` first.")
        else:
            features = pd.DataFrame([{
                "num_medications": len(current_meds),
                "has_duplicate_ingredient": 1 if len(duplicates) > 0 else 0,
                "has_interaction": 1 if len(interactions) > 0 else 0,
                "has_missing_info": 1 if len(missing_info) > 0 else 0,
                "patient_age": patient_age,
                "total_daily_doses": len(current_meds) * 2
            }])

            prediction = model.predict(features)[0]
            proba = model.predict_proba(features)[0]

            labels = {0: "Low Priority Review", 1: "Moderate Priority Review", 2: "High Priority Review"}
            colors = {0: "green", 1: "orange", 2: "red"}

            st.markdown(f"### Priority Assessment: :{colors[prediction]}[{labels[prediction]}]")
            st.metric(label="Model Confidence Level", value=f"{max(proba)*100:.1f}%")

            st.write("**Model Prediction Probabilities:**")
            st.dataframe(pd.DataFrame({
                "Category": ["Low Priority", "Moderate Priority", "High Priority"],
                "Probability": [f"{p*100:.1f}%" for p in proba]
            }))

    st.markdown("---")
    st.caption("🚨 **Disclaimer:** MedSafe is an educational research prototype and portfolio project. "
               "It is not a clinical decision support tool or a substitute for medical advice from a qualified healthcare professional.")
