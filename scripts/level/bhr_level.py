import pandas as pd

df = pd.read_csv("../../files_for_db/geo/bhr_geo.csv")
print(df.shape)
df.head()

def classify_school(row):
    n = str(row['school_name']).lower()
    is_technical = False
    level = "unknown"
    level_detail = None

    # Pre-primary first
    if "kindergarten" in n:
        level = "pre_primary"

    # Schools serving both Primary and Intermediate
    elif "primary" in n and "intermediate" in n:
        level = "mixed"
        level_detail = "primary,lower_secondary"

    # Single-level schools
    elif "primary" in n:
        level = "primary"
    elif "intermediate" in n:
        level = "lower_secondary"
    elif "secondary" in n:
        level = "upper_secondary"

    # Technical / Vocational schools
    if "technical" in n or "vocational" in n:
        level = "upper_secondary"
        is_technical = True

    return pd.Series({
        "school_level": level,
        "school_level_detail": level_detail,
        "is_technical": is_technical
    })

df[["school_level", "school_level_detail", "is_technical"]] = df.apply(classify_school, axis=1)
df["school_level"].value_counts()
df

columns = ["oedc_id", "deped_id", "school_level", "school_level_detail", "is_technical"]

df = df[columns]

df["deped_id"] = df["deped_id"].astype(int)

print(df.head())

df.to_csv("../../files_for_db/level/bhr_level.csv", index = False)