import geopandas as gpd
import pandas as pd
import numpy as np
import zipfile
import shutil
import os

from utils import *


nig_ef = pd.read_csv("../../data/NGA/educational-facilities-in-nigeria.csv")
nig_ef = nig_ef[["facility_name", "facility_type_display", "facility_id", "longitude", "latitude"]]

replacement_map = {
    'Primary school only': 'Primary',
    'Primary and Junior Secondary school combined': 'Primary, Junior Secondary',
    'Primary, Junior and Senior Secondary school combined': 'Primary, Junior Secondary, Senior Secondary',
    "Information not available / Don't know": np.nan,
    'Junior Secondary school only': 'Junior Secondary',
    'Junior and Senior Secondary school combined': 'Junior Secondary, Senior Secondary',
    'Pre-primary and Primary school combined': 'Pre-Primary, Primary',
    'Primary Only': 'Primary',
    'Pre-primary and Primary': 'Pre-Primary, Primary',
    'Primary, Junior, and Senior Secondary': 'Primary, Junior Secondary, Senior Secondary',
    'Adult, Vocational, or Technical': 'Adult, Vocational or Technical',
    'Junior and Senior Secondary': 'Junior Secondary, Senior Secondary',
    'Junior Secondary Only': 'Junior Secondary',
    'Primary and Junior Secondary': 'Primary, Junior Secondary',
    'Pre-primary Only': 'Pre-Primary',
    'Senior Secondary Only': 'Senior Secondary'
}

print(nig_ef["facility_type_display"].unique())

nig_ef['facility_type_display'] = nig_ef['facility_type_display'].replace(replacement_map)

print(nig_ef["facility_type_display"].unique())

nig_ef

print(nig_ef.shape)
nig_ef = nig_ef.drop_duplicates("facility_id")
print(nig_ef.shape)


nig_ef = nig_ef.reset_index()
nig_ef['geo_id'] = nig_ef['index'].apply(lambda x: 'NIG-{0:0>6}'.format(x))
nig_ef["deped_id"] = nig_ef["facility_id"]
nig_ef = nig_ef[["geo_id", "deped_id", "facility_name", "facility_type_display", "longitude", "latitude"]]
nig_ef = nig_ef.rename(columns = {"facility_name":"school_name", "facility_type_display": "school_level"})
nig_ef["address"] = None
nig_ef["adm0"] = "NGA"

print(nig_ef.head())
print(nig_ef.shape)

nig_ef = nig_ef[nig_ef["longitude"] != 0]
nig_ef = nig_ef[nig_ef["latitude"] != 0]

nig_ef = nig_ef.dropna(subset = ["latitude", "longitude"])


print(nig_ef)

longs = nig_ef["longitude"].values
lats = nig_ef["latitude"].values

iso = "NGA"
nig_ef["address"] = None
nig_ef["adm0"] = iso

# Geocode to ADM levels
cols = ["geo_id", "deped_id", "school_name", "school_level", "adm0", "address"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        nig_ef = gpd.GeoDataFrame(nig_ef, geometry = gpd.points_from_xy(nig_ef.longitude, nig_ef.latitude))
        nig_ef = gpd.tools.sjoin(nig_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        nig_ef["longitude"] = longs
        nig_ef["latitude"] = lats
        print(nig_ef.head())


    except Exception as e:

        nig_ef["adm" + str(adm)] = None
        print(e)

nig_ef = nig_ef[["geo_id", "deped_id", "school_name", "school_level", "address", "adm0", "adm1", "adm2", "adm3", "longitude", "latitude"]]

nig_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/nig_geo.csv", index = False)


gdf = gpd.GeoDataFrame(
    nig_ef,
    geometry = gpd.points_from_xy(
        x = nig_ef.longitude,
        y = nig_ef.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/nig/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/nig/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/nig/nig.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/nig", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/nig")
