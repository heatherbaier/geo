import geopandas as gpd
import pandas as pd
import zipfile
import shutil
import os

from utils import *


phl_ef = pd.read_csv("../../data/PHL/this_one.csv")
print(phl_ef.columns)
phl_ef = phl_ef[["school_id", "school_name", "longitude", "latitude", "region", "division", "province"]]
phl_ef = phl_ef.drop_duplicates(subset = ["school_id"])
phl_ef = phl_ef.reset_index()
phl_ef['geo_id'] = phl_ef['index'].apply(lambda x: 'PHL-{0:0>6}'.format(x))
phl_ef["adm0"] = "PHL"
phl_ef["address"] = None
phl_ef = phl_ef[["geo_id", "school_id", "school_name", "address", "adm0", "region", "division", "province", "longitude", "latitude"]].rename(columns = {"school_id": "deped_id", "region": "adm1", "division":"adm2", "province": "adm3"})
phl_ef = phl_ef[["geo_id","deped_id","school_name","address","adm0", "longitude", "latitude"]]
phl_ef = phl_ef[phl_ef["longitude"] != 0]
phl_ef = phl_ef[phl_ef["latitude"] != 0]

print(phl_ef.head())


longs = phl_ef["longitude"].values
lats = phl_ef["latitude"].values

print(phl_ef.head())

# Geocode to ADM levels
iso = "PHL"
phl_ef["adm0"] = iso
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        phl_ef = gpd.GeoDataFrame(phl_ef, geometry = gpd.points_from_xy(phl_ef.longitude, phl_ef.latitude))
        phl_ef = gpd.tools.sjoin(phl_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        phl_ef["longitude"] = longs
        phl_ef["latitude"] = lats
        print(phl_ef.head())


    except Exception as e:

        phl_ef["adm" + str(adm)] = None
        print(e)

phl_ef = phl_ef[["geo_id","deped_id","school_name","address","adm0","adm1","adm2","adm3","longitude","latitude"]]

phl_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/phl_geo.csv", index = False)

gdf = gpd.GeoDataFrame(
    phl_ef,
    geometry = gpd.points_from_xy(
        x = phl_ef.longitude,
        y = phl_ef.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/phl/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/phl/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/phl/phl.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/phl", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/phl")






