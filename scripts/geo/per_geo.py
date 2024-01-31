import geopandas as gpd
import pandas as pd
import zipfile
import shutil
import os

from utils import *


per_ef = pd.read_csv("../../data/PER/Relación de instituciones y programas educativos.csv")
per_ef = per_ef.drop_duplicates(subset = ["cod_mod"])
per_ef['cen_edu'] = per_ef['cen_edu'].str.replace('\d+', '')
per_ef = per_ef[["cen_edu", "cod_mod", "nlong_ie", "nlat_ie"]].rename(columns = {"cod_mod": "deped_id", "cen_edu": "school_name", "nlong_ie": "longitude", "nlat_ie": "latitude"})
per_ef = per_ef[per_ef["longitude"] != 0]
per_ef = per_ef[per_ef["latitude"] != 0]
per_ef = per_ef.dropna(subset = ["latitude", "longitude"])


per_ef = per_ef.reset_index()
per_ef['geo_id'] = per_ef['index'].apply(lambda x: 'PER-{0:0>6}'.format(x))
per_ef = per_ef.drop(["index"], axis = 1)
# per_ef = per_ef[["geo_id", "CODE", "NAME"]].rename(columns = {"CODE": "deped_id", "NAME": "school_name"})
# per_ef = per_ef[["geo_id", "CODE", "NAME", "LONGITUDE", "LATITUDE"]]
# per_ef.columns = ["geo_id", "deped_id", "school_name", "longitude", "latitude"]
per_ef["adm0"] = "PER"
per_ef["address"] = None
print(per_ef.head())

longs = per_ef["longitude"].values
lats = per_ef["latitude"].values

iso = "PER"
per_ef["address"] = None
per_ef["adm0"] = iso

# Geocode to ADM levels
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        per_ef = gpd.GeoDataFrame(per_ef, geometry = gpd.points_from_xy(per_ef.longitude, per_ef.latitude))
        per_ef = gpd.tools.sjoin(per_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        per_ef["longitude"] = longs
        per_ef["latitude"] = lats
        print(per_ef.head())


    except Exception as e:

        per_ef["adm" + str(adm)] = None
        print(e)

per_ef = per_ef[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3", "longitude", "latitude"]]

per_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/per_geo.csv", index = False)


gdf = gpd.GeoDataFrame(
    per_ef,
    geometry = gpd.points_from_xy(
        x = per_ef.longitude,
        y = per_ef.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/per/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/per/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/per/per.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/per", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/per")
