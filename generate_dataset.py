"""
Dataset generator for MedSafe synthetic medication scenarios.
"""
import os
import random
import pandas as pd

MEDICATIONS = [
    {"brand": "Tylenol", "ingredients": ["Acetaminophen"], "dose_mg": 500},
    {"brand": "Panadol", "ingredients": ["Acetaminophen"], "dose_mg": 500},
    {"brand": "Excedrin", "ingredients": ["Acetaminophen", "Aspirin", "Caffeine"], "dose_mg": 250},
    {"brand": "Advil", "ingredients": ["Ibuprofen"], "dose_mg": 200},
    {"brand": "Motrin", "ingredients": ["Ibuprofen"], "dose_mg": 200},
    {"brand": "Aleve", "ingredients": ["Naproxen"], "dose_mg": 220},
    {"brand": "Bayer", "ingredients": ["Aspirin"], "dose_mg": 325},
    {"brand": "Lipitor", "ingredients": ["Atorvastatin"], "dose_mg": 20},
    {"brand": "Zocor", "ingredients": ["Simvastatin"], "dose_mg": 20},
    {"brand": "Crestor", "ingredients": ["Rosuvastatin"], "dose_mg": 10},
    {"brand": "Zestril", "ingredients": ["Lisinopril"], "dose_mg": 10},
    {"brand": "Glucophage", "ingredients": ["Metformin"], "dose_mg": 500},
    {"brand": "Synthroid", "ingredients": ["Levothyroxine"], "dose_mg": 50},
    {"brand": "Norvasc", "ingredients": ["Amlodipine"], "dose_mg": 5},
    {"brand": "Cozaar", "ingredients": ["Losartan"], "dose_mg": 50},
]


def generate_synthetic_data(num_samples: int = 1200, seed: int = 42) -> pd.DataFrame:
    random.seed(seed)
    data = []

    for _ in range(num_samples):
        num_meds = random.choices([1, 2, 3, 4, 5], weights=[0.1, 0.35, 0.35, 0.15, 0.05])[0]
        selected_meds = random.sample(MEDICATIONS, k=min(num_meds, len(MEDICATIONS)))

        total_meds = len(selected_meds)
        has_missing_info = random.random() < 0.15

        all_ingredients = []
        for med in selected_meds:
            all_ingredients.extend(med["ingredients"])

        duplicate_count = len(all_ingredients) - len(set(all_ingredients))
        has_duplicate_ingredient = 1 if duplicate_count > 0 else 0

        known_interaction_pairs = [
            ({"Aspirin", "Ibuprofen"}),
            ({"Aspirin", "Naproxen"}),
            ({"Ibuprofen", "Naproxen"}),
            ({"Atorvastatin", "Simvastatin"}),
        ]
        
        has_interaction = 0
        ing_set = set(all_ingredients)
        for pair in known_interaction_pairs:
            if pair.issubset(ing_set):
                has_interaction = 1
                break

        patient_age = random.randint(18, 88)
        daily_doses_count = sum([random.choice([1, 2, 3]) for _ in selected_meds])

        # Risk Classification Logic
        # 0 = Low, 1 = Moderate, 2 = High
        if (has_duplicate_ingredient and has_interaction) or (total_meds >= 4 and has_interaction):
            review_priority = 2
        elif has_duplicate_ingredient or has_interaction or total_meds >= 4 or (patient_age > 70 and total_meds >= 3):
            review_priority = 1
        else:
            review_priority = 0

        data.append({
            "num_medications": total_meds,
            "has_duplicate_ingredient": has_duplicate_ingredient,
            "has_interaction": has_interaction,
            "has_missing_info": 1 if has_missing_info else 0,
            "patient_age": patient_age,
            "total_daily_doses": daily_doses_count,
            "review_priority": review_priority
        })

    return pd.DataFrame(data)


if __name__ == "__main__":
    df = generate_synthetic_data()
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/synthetic_medications.csv", index=False)
    print(f"Dataset generated successfully at 'data/synthetic_medications.csv' with {len(df)} rows.")
