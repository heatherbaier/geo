import geopandas as gpd
import pandas as pd
import numpy as np
import zipfile
import shutil
import os

from utils import *


tun_ef = pd.read_csv("../../data/TUN/gps_etablissements_scolaires.csv")
tun_ef = tun_ef[["code_etablissement", "nom_etablissement", "Longitude initiale", "Latitude initiale"]]
tun_ef = tun_ef.drop_duplicates(subset = ["code_etablissement"])
tun_ef = tun_ef.reset_index()
tun_ef['geo_id'] = tun_ef['index'].apply(lambda x: 'TUN-{0:0>6}'.format(x))
tun_ef = tun_ef.drop(["index"], axis = 1)
tun_ef.columns = ["deped_id", "school_name", "longitude", "latitude", "geo_id"]
tun_ef = tun_ef[["geo_id", "deped_id", "school_name", "longitude", "latitude"]]


tun_ef["latitude"].astype(str).str[0:2] + "." + tun_ef["latitude"].astype(str).str[2:]

print(tun_ef.shape)

tun_ef["latitude"] = pd.to_numeric(tun_ef["latitude"].astype(str).str.replace(",", ".").str.strip(), errors = 'coerce')#.astype(float, errors = "ignore")
tun_ef["longitude"] = pd.to_numeric(tun_ef["longitude"].astype(str).str.replace(",", ".").str.strip(), errors = 'coerce')#.astype(float, errors = "ignore")
tun_ef = tun_ef.dropna(subset = ["longitude", "latitude"])

print(tun_ef.shape)

# tun_ef["latitude"] = np.where(tun_ef["latitude"].str.contains("."), tun_ef["latitude"], tun_ef["latitude"].astype(str).str[0:2] + "." + tun_ef["latitude"].astype(str).str[2:])

tun_ef["address"] = None


print(tun_ef.tail(50))

tun_ef.to_csv("./test_tun2.csv")


# asga


tun_ef = tun_ef[tun_ef["longitude"] != 0]
tun_ef = tun_ef[tun_ef["latitude"] != 0]

tun_ef = tun_ef.dropna(subset = ["latitude", "longitude"])
tun_ef["address"] = None
tun_ef["adm0"] = "tun"

print(tun_ef.head())

# Geocode to ADM levels
longs = tun_ef["longitude"].values
lats = tun_ef["latitude"].values

iso = "TUN"
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        tun_ef = gpd.GeoDataFrame(tun_ef, geometry = gpd.points_from_xy(tun_ef.longitude, tun_ef.latitude))
        tun_ef = gpd.tools.sjoin(tun_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        tun_ef["longitude"] = longs
        tun_ef["latitude"] = lats
        print(tun_ef.head())


    except Exception as e:

        tun_ef["adm" + str(adm)] = None
        print(e)

tun_ef = tun_ef[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3", "longitude", "latitude"]]

tun_ef = tun_ef.dropna(subset = ["adm1"])


tun_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/tun_geo.csv", index = False, encoding = "UTF-8")


gdf = gpd.GeoDataFrame(
    tun_ef,
    geometry = gpd.points_from_xy(
        x = tun_ef.longitude,
        y = tun_ef.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tun/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tun/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tun/tun.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tun", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tun")


