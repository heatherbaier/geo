import geopandas as gpd
import pandas as pd

df = pd.read_csv("../../files_for_db/geo/blz_geo.csv")
print(df.head())

gdf = gpd.read_file("../../data/BLZ/schools.geojson")[["Code", "Level_"]].rename(columns = {"Code": "deped_id"})
print(gdf.head())

df = pd.merge(df, gdf, on = "deped_id")
print(df.head())

def classify_belize_school(row):
    """
    Classify Belize schools into ISCED-aligned levels (0-3) and flag vocational programs.
    Excludes tertiary and adult/continuing education from GEO.
    """
    level_raw = str(row['Level_']).strip().lower()
    is_technical = False
    school_level = "unknown"
    detail = None
    confidence = "high"

    # Map based on known categories
    if level_raw == "preschool":
        school_level = "pre_primary"        # ISCED 0
    elif level_raw == "primary":
        school_level = "primary"           # ISCED 1
    elif level_raw == "secondary":
        school_level = "upper_secondary"   # ISCED 3
    elif level_raw == "vocational":
        school_level = "upper_secondary"   # ISCED 3 (vocational)
        is_technical = True
    elif level_raw in ["tertiary", "adult and continuing"]:
        # Explicit exclusion
        school_level = "excluded"
        confidence = "n/a"
    else:
        school_level = "unknown"
        confidence = "low"

    return pd.Series({
        "school_level": school_level,
        "school_level_detail": detail,
        "is_technical": is_technical,
        "classification_confidence": confidence
    })

# Apply to your dataframe
df[["school_level", "school_level_detail", "is_technical", "classification_confidence"]] = (
    df.apply(classify_belize_school, axis=1)
)

df = df[["oedc_id", "deped_id", "school_level", "school_level_detail", "is_technical"]]

print(df.head())

df.to_csv("../../files_for_db/level/blz_level.csv", index = False)
