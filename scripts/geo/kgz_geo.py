from utils import *

import geopandas as gpd
import pandas as pd
import shutil
import os

DATA_PATH = str(os.path.abspath(os.path.join(__file__ ,"../../.."))) + "/data/KGZ/kgz_edufac_unicef_shp/"
kgz_ef = gpd.read_file(DATA_PATH + "kgz_edufac_unicef.shp")

kgz_ef = kgz_ef[["school_loc", "Longitude", "Latitude", "school_nam","school_ID"]]
kgz_ef.columns = ["address", "longitude", "latitude", "school_name","deped_id"]
kgz_ef = kgz_ef[kgz_ef["longitude"] != 0]
kgz_ef = kgz_ef[kgz_ef["latitude"] != 0]








# Generate GEO ID's
kgz_ef = kgz_ef.reset_index()
kgz_ef['geo_id'] = kgz_ef['index'].apply(lambda x: 'KGZ-{0:0>6}'.format(x))
kgz_ef = kgz_ef[["geo_id", "deped_id", "school_name", "latitude", "longitude","address"]]


longs = kgz_ef["longitude"].values
lats = kgz_ef["latitude"].values

# Geocode to ADM levels
iso = "KGZ"
kgz_ef["adm0"] = iso
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
for adm in range(1, 4):

    try:
        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), ".")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "."))
        kgz_ef = gpd.GeoDataFrame(kgz_ef, geometry = gpd.points_from_xy(kgz_ef.longitude, kgz_ef.latitude))
        kgz_ef = gpd.tools.sjoin(kgz_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        kgz_ef["longitude"] = longs
        kgz_ef["latitude"] = lats
        print(kgz_ef.head())

    except Exception as e:

        kgz_ef["adm" + str(adm)] = None
        print(e)


kgz_ef = kgz_ef[["geo_id","deped_id","school_name","address","adm0","adm1","adm2","adm3","longitude","latitude"]]


PATH = str(os.path.abspath(os.path.join(__file__ ,"../../..")))
print("PATH: ", PATH)
kgz_ef.to_csv(PATH + "/files_for_db/geo/kgz_geo.csv", index = False)

# kgz_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/kgz_geo.csv", index = False)

gdf = gpd.GeoDataFrame(
    kgz_ef,
    geometry = gpd.points_from_xy(
        x = kgz_ef.longitude,
        y = kgz_ef.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)



if not os.path.exists(PATH + "/files_for_db/shps/kgz/"):
    os.mkdir(PATH + "/files_for_db/shps/kgz/")

# Add shape file to files_for_db
gdf.to_file(PATH + "/files_for_db/shps/kgz/kgz.shp", index = False)

# Add zip file to files_for_db
shutil.make_archive(PATH + "/files_for_db/shps/kgz", 'zip', PATH + "/files_for_db/shps/kgz")



# if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/kgz/"):
#     os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/kgz/")

# gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/kgz/kgz.shp", index = False)

# shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/kgz", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/kgz")

