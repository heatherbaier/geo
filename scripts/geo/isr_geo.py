import geopandas as gpd
import pandas as pd
import zipfile
import shutil
import os

from utils import *



isr_ef = pd.read_csv("../../data/ISR/moe_mosdot_coordinates.csv")
isr_ef = isr_ef[["SEMEL_MOSAD", "SHEM_MOSAD", "UTM_X", "UTM_Y"]]
isr_ef.columns = ["deped_id", "school_name", "longitude", "latitude"]
isr_ef = isr_ef.drop_duplicates(subset = ["deped_id"])
isr_ef = isr_ef.reset_index()
isr_ef['geo_id'] = isr_ef['index'].apply(lambda x: 'ISR-{0:0>6}'.format(x))
isr_ef = isr_ef.drop(["index"], axis = 1)
# isr_ef = isr_ef[["geo_id", "CODE", "NAME"]].rename(columns = {"CODE": "deped_id", "NAME": "school_name"})
# isr_ef = isr_ef[["geo_id", "CODE", "NAME", "LONGITUDE", "LATITUDE"]]
print(isr_ef.head())

# asga

longs = isr_ef["longitude"].values
lats = isr_ef["latitude"].values

iso = "ISR"
isr_ef["address"] = None
isr_ef["adm0"] = iso

# Geocode to ADM levels
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        isr_ef = gpd.GeoDataFrame(isr_ef, geometry = gpd.points_from_xy(isr_ef.longitude, isr_ef.latitude))
        isr_ef = gpd.tools.sjoin(isr_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        isr_ef["longitude"] = longs
        isr_ef["latitude"] = lats
        print(isr_ef.head())


    except Exception as e:

        isr_ef["adm" + str(adm)] = None
        print(e)

isr_ef = isr_ef[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3", "longitude", "latitude"]]

isr_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/isr_geo.csv", index = False)


gdf = gpd.GeoDataFrame(
    isr_ef,
    geometry = gpd.points_from_xy(
        x = isr_ef.longitude,
        y = isr_ef.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/isr/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/isr/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/isr/isr.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/isr", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/isr")




