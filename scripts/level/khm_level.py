import geopandas as gpd
import pandas as pd
import shutil
import os


# Fetch and read the datasets
DATA_PATH = str(os.path.abspath(os.path.join(__file__ ,"../../.."))) + "/data/KHM/"
khm_schools = gpd.read_file(DATA_PATH + "2014/Basic information of school (2014)/basic_information_of_school_2014.shp")
khm_schools = khm_schools.to_crs("epsg:4326")


geo = pd.read_csv("../../files_for_db/geo/khm_geo.csv")[["geo_id", "deped_id"]]


type_map = {
    "Pre school": "pre_primary",
    "Primary": "primary",
    "College": "lower_secondary",
    "Lycee G7-12": "mixed",           # spans ISCED 2+3
    "Lycee G10-12": "upper_secondary"
}

khm_schools["school_level"] = khm_schools["SCHOOL_TYP"].map(type_map)

print(khm_schools["school_level"].value_counts())

khm_schools = khm_schools[["SCHOOL_COD", "school_level"]].rename(columns = {"SCHOOL_COD": "deped_id"})

khm_schools = pd.merge(geo, khm_schools, on = "deped_id")

print(khm_schools.head())

khm_schools.to_csv("../../files_for_db/level/khm_level.csv", index = False)
