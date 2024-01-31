import geopandas as gpd
import pandas as pd
import zipfile
import shutil
import os

from utils import *


#import necessary data from github
zaf_table = pd.read_excel("/Users/heatherbaier/Documents/geo_git/data/ZAF/National.xlsx")
# zaf_ids = pd.read_csv("../../files_for_db/ids/zaf_ids.csv")

#select and rename necessary columns
zaf_table = zaf_table[["NatEmis", "Official_Institution_Name", "StreetAddress", "GIS_Long", "GIS_Lat"]]
zaf_table.columns = ["deped_id", "school_name", "address", "longitude", "latitude"]

zaf_table = zaf_table.drop_duplicates(subset = ["deped_id"])
zaf_table = zaf_table.reset_index()
zaf_table['geo_id'] = zaf_table['index'].apply(lambda x: 'ZAF-{0:0>6}'.format(x))
zaf_table = zaf_table.drop(["index"], axis = 1)
# zaf_table = zaf_table[["geo_id", "CODE", "NAME"]].rename(columns = {"CODE": "deped_id", "NAME": "school_name"})
# zaf_table = zaf_table[["geo_id", "CODE", "NAME", "LONGITUDE", "LATITUDE"]]
# zaf_table.columns = ["geo_id", "deped_id", "school_name", "longitude", "latitude"]
# zaf_table["school_name"] = None


zaf_table = zaf_table[zaf_table["longitude"] != 0]
zaf_table = zaf_table[zaf_table["latitude"] != 0]

zaf_table = zaf_table.dropna(subset = ["latitude", "longitude"])


print(zaf_table)

longs = zaf_table["longitude"].values
lats = zaf_table["latitude"].values

iso = "ZAF"
zaf_table["adm0"] = iso

print(zaf_table.head())
print(zaf_table.columns)



# Geocode to ADM levels
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        zaf_table = gpd.GeoDataFrame(zaf_table, geometry = gpd.points_from_xy(zaf_table.longitude, zaf_table.latitude))
        zaf_table = gpd.tools.sjoin(zaf_table, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        zaf_table["longitude"] = longs
        zaf_table["latitude"] = lats
        print(zaf_table.head())


    except Exception as e:

        zaf_table["adm" + str(adm)] = None
        print(e)

zaf_table = zaf_table[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3", "longitude", "latitude"]]

zaf_table.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/zaf_geo.csv", index = False)


gdf = gpd.GeoDataFrame(
    zaf_table,
    geometry = gpd.points_from_xy(
        x = zaf_table.longitude,
        y = zaf_table.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/zaf/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/zaf/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/zaf/zaf.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/zaf", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/zaf")
