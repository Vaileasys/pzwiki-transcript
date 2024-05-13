# dictionary to map moodles
CODES_REPLACEMENTS = {
    "BOR": "Boredom",
    "STS": "Stress",
    "UHP": "Unhappiness",
    "PAN": "Panic",
    "FEA": "Fear",
    "FAT": "Fatigue",
    "COO": "Cooking", #skill
    "CRP": "Carpentry", #skill
    "FIS": "Fishing", #skill
    "FRM": "Farming", #skill
    "FOD": "Foraging", #skill
    "TRA": "Trapping", #skill
    "MEC": "Mechanics", #skill
    "TAI": "Tailoring", #skill
    "TAI": "Metalworking", #skill
    "TAI": "Electrical", #skill
    "DOC": "First Aid", #skill
    "LFT": "Lightfooted", #skill
    "AIM": "Aiming", #skill
    "REL": "Reloading", #skill
    "RCP": "RCP", #recipe e.g. "RCP=Make Cake Batter"
}

def replace_codes(code_part):
    return CODES_REPLACEMENTS.get(code_part, code_part)
