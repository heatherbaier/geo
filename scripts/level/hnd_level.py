import geopandas as gpd
import pandas as pd
import shutil
import os

data = pd.read_excel("../../data/HND/coordenadasporcentroeducativo_siplie_23marzo2020.xlsx", header=6)
print(data["Nivel"].unique())

import pandas as pd
import numpy as np

def classify_honduras_school(row):
    raw = str(row['Nivel']) if pd.notna(row['Nivel']) else ""
    raw_upper = raw.upper()
    levels = set()
    offers_adult = "ADULTOS" in raw_upper

    # Pre-Básica (pre-primary)
    if "PRE-BÁSICA" in raw_upper or "CCPREB" in raw_upper:
        levels.add("pre_primary")
    # Básica (grades 1–9, even if adult modality present)
    if "BÁSICA" in raw_upper:
        levels.add("primary")
        levels.add("lower_secondary")
    # Media (upper secondary)
    if "MEDIA" in raw_upper:
        levels.add("upper_secondary")

    if not levels:
        school_level = "unknown"
    elif len(levels) == 1:
        school_level = list(levels)[0]
    else:
        school_level = "mixed"

    return pd.Series({
        "school_level": school_level,
        "school_level_detail": ",".join(sorted(levels)) if len(levels) > 1 else None,
        "offers_adult_program": offers_adult
    })

data[["school_level", "school_level_detail", "offers_adult_program"]] = data.apply(classify_honduras_school, axis=1)


print(data["school_level"].unique())
print(data["school_level_detail"].unique())
print(data["school_level"].value_counts())

data.to_csv("../../files_for_db/level/hnd_level.csv", index = False)