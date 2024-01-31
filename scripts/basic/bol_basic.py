import geopandas as gpd
import pandas as pd
import os

from utils import *


iso = "BOL"
bol_ef = pd.read_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/ids/bol_ids.csv")
bol_ef["adm0"] = iso
bol_ef["address"] = None

print(bol_ef.head())

coords = pd.read_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/coordinates/bol_coordinates.csv")
bol_ef = pd.merge(bol_ef, coords, on = "geo_id")


bol_ef = bol_ef[["geo_id", "deped_id", "school_name", "address", "adm0"]]

print(bol_ef.head())


longs = bol_ef["longitude"].values
lats = bol_ef["latitude"].values

# Geocode to ADM levels
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        bol_ef = gpd.GeoDataFrame(bol_ef, geometry = gpd.points_from_xy(bol_ef.longitude, bol_ef.latitude))
        bol_ef = gpd.tools.sjoin(bol_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        bol_ef["longitude"] = longs
        bol_ef["latitude"] = lats
        print(bol_ef.head())


    except Exception as e:

        bol_ef["adm" + str(adm)] = None
        print(e)

bol_ef = bol_ef[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3"]]

# bol_ef = bol_ef[cols].drop(["longitude", "latitude"], axis = 1)

bol_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/basic/bol_basic.csv", index = False)

