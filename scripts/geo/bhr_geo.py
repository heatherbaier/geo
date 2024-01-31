import geopandas as gpd
import pandas as pd
import zipfile
import shutil
import os

from utils import *


bhr_ef = pd.read_csv("../../data/BHR/bahrain_school_locations.csv")
bhr_ef = bhr_ef[bhr_ef["SUBTYPE EN"].isin(["KINDERGARTEN", "PUBLIC SCHOOLS - BOYS", "PUBLIC SCHOOLS - GIRLS"])]
bhr_ef = bhr_ef[['NAME', "#", "POINT_X_Longitude", "POINT_Y_Latitude"]]
bhr_ef = bhr_ef.drop_duplicates(subset = ["POINT_X_Longitude", "POINT_Y_Latitude"])
bhr_ef = bhr_ef.reset_index()
bhr_ef['geo_id'] = bhr_ef['index'].apply(lambda x: 'BHR-{0:0>6}'.format(x))
bhr_ef = bhr_ef.drop(["index"], axis = 1)
bhr_ef = bhr_ef[["geo_id", "#", "NAME", "POINT_X_Longitude", "POINT_Y_Latitude"]].rename(columns = {"#": "deped_id", "NAME": "school_name", "POINT_X_Longitude": "longitude", "POINT_Y_Latitude": "latitude"})
bhr_ef["address"] = None
bhr_ef["adm0"] = "BHR"

bhr_ef = bhr_ef[bhr_ef["longitude"] != 0]
bhr_ef = bhr_ef[bhr_ef["latitude"] != 0]

longs = bhr_ef["longitude"].values
lats = bhr_ef["latitude"].values

print(bhr_ef.head())

# Geocode to ADM levels
iso = "BHR"
bhr_ef["adm0"] = iso
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        bhr_ef = gpd.GeoDataFrame(bhr_ef, geometry = gpd.points_from_xy(bhr_ef.longitude, bhr_ef.latitude))
        bhr_ef = gpd.tools.sjoin(bhr_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        bhr_ef["longitude"] = longs
        bhr_ef["latitude"] = lats
        print(bhr_ef.head())


    except Exception as e:

        bhr_ef["adm" + str(adm)] = None
        print(e)

bhr_ef = bhr_ef[["geo_id","deped_id","school_name","address","adm0","adm1","adm2","adm3","longitude","latitude"]]

bhr_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/bhr_geo.csv", index = False)

gdf = gpd.GeoDataFrame(
    bhr_ef,
    geometry = gpd.points_from_xy(
        x = bhr_ef.longitude,
        y = bhr_ef.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/bhr/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/bhr/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/bhr/bhr.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/bhr", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/bhr")



