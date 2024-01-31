import geopandas as gpd
import pandas as pd
import zipfile
import shutil
import os

from utils import *


sle_ef = pd.read_csv("../../data/SLE/sleeducptstewardschools.csv")
sle_ef = sle_ef[["Educ_Code", "Educ_Name", "Longitude", "Latitude"]]
sle_ef = sle_ef.drop_duplicates(subset = ["Educ_Code"])
sle_ef = sle_ef.reset_index()
sle_ef['geo_id'] = sle_ef['index'].apply(lambda x: 'SLE-{0:0>6}'.format(x))
sle_ef = sle_ef.drop(["index"], axis = 1)
sle_ef.columns = ["deped_id", "school_name", "longitude", "latitude", "geo_id"]
sle_ef = sle_ef[["geo_id", "deped_id", "school_name", "longitude", "latitude"]]
sle_ef = sle_ef[sle_ef["longitude"] != 0]
sle_ef = sle_ef[sle_ef["latitude"] != 0]

sle_ef = sle_ef.dropna(subset = ["latitude", "longitude"])
sle_ef["address"] = None
sle_ef["adm0"] = "SLE"

print(sle_ef.head())

# Geocode to ADM levels
longs = sle_ef["longitude"].values
lats = sle_ef["latitude"].values

iso = "SLE"
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        sle_ef = gpd.GeoDataFrame(sle_ef, geometry = gpd.points_from_xy(sle_ef.longitude, sle_ef.latitude))
        sle_ef = gpd.tools.sjoin(sle_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        sle_ef["longitude"] = longs
        sle_ef["latitude"] = lats
        print(sle_ef.head())


    except Exception as e:

        sle_ef["adm" + str(adm)] = None
        print(e)

sle_ef = sle_ef[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3", "longitude", "latitude"]]

sle_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/sle_geo.csv", index = False)


gdf = gpd.GeoDataFrame(
    sle_ef,
    geometry = gpd.points_from_xy(
        x = sle_ef.longitude,
        y = sle_ef.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/sle/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/sle/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/sle/sle.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/sle", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/sle")


