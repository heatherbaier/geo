import pandas as pd
from utils import *

#import and format data from github
with open("../../data/KEN/schools.json") as schools_raw:
    schools_raw = schools_raw.read()[96:-1]
ken_table = pd.read_json(schools_raw)

ken_id_table = pd.read_csv("../../files_for_db/ids/ken_ids.csv")

#extract info from dictionaries to create columns
ken_table["longitude"] = None
ken_table["latitude"] = None
for i in range(len(ken_table)):
    ken_table["longitude"].iloc[i] = ken_table["properties"].iloc[i]["Y_Coord"]
    ken_table["latitude"].iloc[i] = ken_table["properties"].iloc[i]["X_Coord"]

#merge tables to get geoid
ken_table["country_id"] = ken_table["id"]
ken_table_coordinates = pd.merge(ken_table, ken_id_table, how="inner")
ken_table_coordinates = ken_table_coordinates[["geo_id", "longitude", "latitude"]]

#export as csv
ken_table_coordinates.to_csv("../../files_for_db/coordinates/ken_coordinates.csv", index=False)
