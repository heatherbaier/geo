import geopandas as gpd
import pandas as pd
import shutil
import os

from utils import *


# Clean coordinates
bol_ef = gpd.read_file("/Users/heatherbaier/Documents/geo_git/data/BOL/EstabEducativos/EstabEducativos.shp")

print()




bol_ef = bol_ef[["gml_id", "ESTABLECIM", "POINT_X", "POINT_Y"]]
bol_ef.columns = ["deped_id", "school_name", "longitude", "latitude"]
bol_ef = bol_ef[bol_ef["longitude"] != 0]
bol_ef = bol_ef[bol_ef["latitude"] != 0]


# Generate GEO ID's
bol_ef = bol_ef.reset_index()
bol_ef['geo_id'] = bol_ef['index'].apply(lambda x: 'BOL-{0:0>6}'.format(x))
bol_ef = bol_ef[["geo_id", "deped_id", "school_name", "latitude", "longitude"]].rename(columns = {"gml_id": "deped_id"})
bol_ef["address"] = None

print(bol_ef.head())

longs = bol_ef["longitude"].values
lats = bol_ef["latitude"].values

# Geocode to ADM levels
iso = "BOL"
bol_ef["adm0"] = iso
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

bol_ef = bol_ef[["geo_id","deped_id","school_name","address","adm0","adm1","adm2","adm3","longitude","latitude"]]

bol_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/bol_geo.csv", index = False)

gdf = gpd.GeoDataFrame(
    bol_ef,
    geometry = gpd.points_from_xy(
        x = bol_ef.longitude,
        y = bol_ef.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/bol/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/bol/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/bol/bol.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/bol", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/bol")