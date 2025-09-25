"""
Game Names Database
Contains period-appropriate names for different eras
"""

import yaml
from pathlib import Path

# Period names loaded from yaml
PERIOD_NAMES = []

def load_period_names():
    """Load period names from YAML file"""
    yaml_file = Path("npcs/period_names.yml")
    if yaml_file.exists():
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
            if data:
                return data
    return []

# Load names on module import
PERIOD_NAMES = load_period_names()

def get_names_for_year(year):
    """Get appropriate names for a given year"""
    # Simple era mapping
    if year < 1985:
        era = "early_80s"
    elif year < 1990:
        era = "late_80s"
    elif year < 1995:
        era = "early_90s"
    elif year < 2000:
        era = "late_90s"
    elif year < 2005:
        era = "early_2000s"
    elif year < 2010:
        era = "late_2000s"
    elif year < 2018:
        era = "early_2010s"
    elif year < 2025:
        era = "late_2010s"
    else:
        era = "future"

    # Return subset of names based on era
    # For now, just return a slice of the full list
    if era in ["early_80s", "late_80s"]:
        return PERIOD_NAMES[:50]
    elif era in ["early_90s", "late_90s"]:
        return PERIOD_NAMES[20:80]
    elif era in ["early_2000s", "late_2000s"]:
        return PERIOD_NAMES[40:120]
    elif era in ["early_2010s", "late_2010s"]:
        return PERIOD_NAMES[80:180]
    else:
        return PERIOD_NAMES[100:]

def get_all_period_names():
    """Get all period names"""
    return PERIOD_NAMES

def get_total_names():
    """Get total count of period names"""
    return len(PERIOD_NAMES)