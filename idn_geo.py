from utils import *
import geopandas as gpd
import pandas as pd
import shutil
import os

DATA_PATH = str(os.path.abspath(os.path.join(__file__ ,"../../.."))) + "/data/IDN/IDN_school_facilities/"
idn_ef = gpd.read_file(DATA_PATH + "IDN_school_facilities.shp")

idn_ef = idn_ef[["ADDRESS", "Longitude", "Latitude", "NAME"]]
idn_ef.columns = ["address", "longitude", "latitude", "school_name"]
idn_ef = idn_ef[idn_ef["longitude"] != 0]
idn_ef = idn_ef[idn_ef["latitude"] != 0]


# Generate GEO ID's
idn_ef = idn_ef.reset_index()
idn_ef['geo_id'] = idn_ef['index'].apply(lambda x: 'IDN-{0:0>6}'.format(x))
idn_ef["deped_id"] = None
idn_ef = idn_ef[["geo_id", "deped_id", "school_name", "latitude", "longitude","address"]]

longs = idn_ef["longitude"].values
lats = idn_ef["latitude"].values



# Geocode to ADM levels
iso = "IDN"
idn_ef["adm0"] = iso
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
for adm in range(1, 4):

    try:
        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), ".")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "."))
        idn_ef = gpd.GeoDataFrame(idn_ef, geometry = gpd.points_from_xy(idn_ef.longitude, idn_ef.latitude))
        idn_ef = gpd.tools.sjoin(idn_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        idn_ef["longitude"] = longs
        idn_ef["latitude"] = lats
        print(idn_ef.head())

    except Exception as e:

        idn_ef["adm" + str(adm)] = None
        print(e)

idn_ef = idn_ef[["geo_id","deped_id","school_name","address","adm0","adm1","adm2","adm3","longitude","latitude"]]

idn_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/idn_geo.csv", index = False)

gdf = gpd.GeoDataFrame(
    idn_ef,
    geometry = gpd.points_from_xy(
        x = idn_ef.longitude,
        y = idn_ef.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/idn/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/idn/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/idn/idn.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/idn", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/idn")