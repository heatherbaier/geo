import geopandas as gpd
import pandas as pd
import zipfile
import shutil
import os

from utils import *


#import necessary data from github
pry_raw = pd.read_csv("../../data/PRY/pry_coords.csv")
pry_raw = pry_raw[["codigo_est", "direccion", "ycoord", "xcoord"]]
pry_raw.columns = ["deped_id", "address", "latitude", "longitude"]
pry_raw = pry_raw.drop_duplicates(subset = ["deped_id"])
pry_raw = pry_raw.reset_index()
pry_raw = pry_raw[pry_raw["longitude"] != 0]
pry_raw = pry_raw[pry_raw["latitude"] != 0]
pry_raw = pry_raw.dropna(subset = ["latitude", "longitude"])
pry_raw['index'] = [i for i in range(len(pry_raw))]
pry_raw['geo_id'] = pry_raw['index'].apply(lambda x: 'PRY-{0:0>6}'.format(x))

print(pry_raw)

# dasga

pry_raw = pry_raw.drop(["index"], axis = 1)
# pry_raw = pry_raw[["geo_id", "CODE", "NAME"]].rename(columns = {"CODE": "deped_id", "NAME": "school_name"})
# pry_raw = pry_raw[["geo_id", "CODE", "NAME", "LONGITUDE", "LATITUDE"]]
# pry_raw.columns = ["geo_id", "deped_id", "school_name", "longitude", "latitude"]
pry_raw["school_name"] = None
print(pry_raw.head())
print(pry_raw.columns)





print(pry_raw)

longs = pry_raw["longitude"].values
lats = pry_raw["latitude"].values

iso = "PRY"
pry_raw["address"] = None
pry_raw["adm0"] = iso

# Geocode to ADM levels
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        pry_raw = gpd.GeoDataFrame(pry_raw, geometry = gpd.points_from_xy(pry_raw.longitude, pry_raw.latitude))
        pry_raw = gpd.tools.sjoin(pry_raw, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        pry_raw["longitude"] = longs
        pry_raw["latitude"] = lats
        print(pry_raw.head())


    except Exception as e:

        pry_raw["adm" + str(adm)] = None
        print(e)

pry_raw = pry_raw[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3", "longitude", "latitude"]]

pry_raw.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/pry_geo.csv", index = False)


gdf = gpd.GeoDataFrame(
    pry_raw,
    geometry = gpd.points_from_xy(
        x = pry_raw.longitude,
        y = pry_raw.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/pry/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/pry/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/pry/pry.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/pry", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/pry")
