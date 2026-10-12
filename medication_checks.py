"""
Deterministic medication rule-based safety check module.
Checks duplicate active ingredients, missing information, and verified interactions.
"""
from typing import List, Dict, Any


KNOWN_INTERACTIONS = [
    {
        "pair": {"Aspirin", "Ibuprofen"},
        "severity": "High",
        "description": "Concomitant use of Aspirin and Ibuprofen may reduce the cardioprotective effects of Aspirin and increase gastrointestinal bleeding risk."
    },
    {
        "pair": {"Aspirin", "Naproxen"},
        "severity": "High",
        "description": "Combining NSAIDs like Aspirin and Naproxen increases the risk of upper gastrointestinal ulceration and bleeding."
    },
    {
        "pair": {"Ibuprofen", "Naproxen"},
        "severity": "Moderate",
        "description": "Using multiple NSAIDs together increases toxicity without offering additional therapeutic benefit."
    },
    {
        "pair": {"Atorvastatin", "Simvastatin"},
        "severity": "High",
        "description": "Combining multiple statins significantly increases the risk of myopathy and rhabdomyolysis."
    }
]


def check_duplicate_ingredients(medications: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Identifies when two or more products list the same active ingredient."""
    ingredient_map = {}
    duplicates = []

    for med in medications:
        med_name = med.get("name", "Unknown Medication")
        ingredients = med.get("ingredients", [])
        for ing in ingredients:
            ing_clean = ing.strip().title()
            if ing_clean in ingredient_map:
                ingredient_map[ing_clean].append(med_name)
            else:
                ingredient_map[ing_clean] = [med_name]

    for ing, med_list in ingredient_map.items():
        if len(med_list) > 1:
            duplicates.append({
                "ingredient": ing,
                "found_in": med_list,
                "message": f"Duplicate Active Ingredient Detected: '{ing}' is present in {', '.join(med_list)}."
            })

    return duplicates


def check_missing_info(medications: List[Dict[str, Any]]) -> List[str]:
    """Flags incomplete medication details such as missing dosage or active ingredients."""
    missing_flags = []
    for idx, med in enumerate(medications, start=1):
        med_name = med.get("name", f"Medication #{idx}")
        if not med.get("ingredients"):
            missing_flags.append(f"'{med_name}' is missing active ingredient information.")
        if not med.get("dosage"):
            missing_flags.append(f"'{med_name}' is missing dosage information.")
    return missing_flags


def check_drug_interactions(medications: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Checks input medications against verified reference interaction rules."""
    all_ingredients = set()
    for med in medications:
        for ing in med.get("ingredients", []):
            all_ingredients.add(ing.strip().title())

    found_interactions = []
    for rule in KNOWN_INTERACTIONS:
        if rule["pair"].issubset(all_ingredients):
            found_interactions.append({
                "drugs": list(rule["pair"]),
                "severity": rule["severity"],
                "description": rule["description"]
            })

    return found_interactions
