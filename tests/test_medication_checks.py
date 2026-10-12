"""
Automated unit tests for medication deterministic safety checks.
"""
from medication_checks import (
    check_duplicate_ingredients,
    check_missing_info,
    check_drug_interactions
)


def test_duplicate_ingredients():
    meds = [
        {"name": "Tylenol", "ingredients": ["Acetaminophen"], "dosage": "500mg"},
        {"name": "Excedrin", "ingredients": ["Acetaminophen", "Caffeine"], "dosage": "250mg"}
    ]
    duplicates = check_duplicate_ingredients(meds)
    assert len(duplicates) == 1
    assert duplicates[0]["ingredient"] == "Acetaminophen"


def test_missing_info():
    meds = [
        {"name": "Meda", "ingredients": [], "dosage": "500mg"},
        {"name": "Medb", "ingredients": ["Aspirin"], "dosage": ""}
    ]
    missing = check_missing_info(meds)
    assert len(missing) == 2


def test_drug_interactions():
    meds = [
        {"name": "Bayer", "ingredients": ["Aspirin"], "dosage": "325mg"},
        {"name": "Advil", "ingredients": ["Ibuprofen"], "dosage": "200mg"}
    ]
    interactions = check_drug_interactions(meds)
    assert len(interactions) == 1
    assert interactions[0]["severity"] == "High"
