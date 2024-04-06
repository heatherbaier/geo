import geopandas as gpd
import pandas as pd
import shutil
import os

from utils import *

# import data
yem = gpd.read_file("../../data/YEM/ymn-edu-facility/ymn-edu-facility.shp")

# select and rename necessary columns
yem = yem[["ID_STL", "x", "y"]]
yem.columns = ["deped_id", "longitude", "latitude"]

# create new columns
yem["school_name"] = None
yem["address"] = None
yem["adm0"] = "YEM"

# create geo_ids
yem.reset_index(inplace=True)
yem["geo_id"] = yem['index'].apply(lambda x: 'YEM-{0:0>6}'.format(x))
yem = yem.drop(columns="index")

# retrieve adms
longs = yem["longitude"].values
lats = yem["latitude"].values
cols = ["deped_id", "longitude", "latitude", "school_name", "address", "adm0", "geo_id"]
for adm in range(1, 4):
    try:
        cols += ["adm" + str(adm)]
        downloadGB("YEM", str(adm), ".")
        shp = gpd.read_file(getGBpath("YEM", f"ADM{str(adm)}", "."))
        yem = gpd.GeoDataFrame(yem, geometry = gpd.points_from_xy(yem.longitude, yem.latitude))
        yem = gpd.tools.sjoin(yem, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        yem["longitude"] = longs
        yem["latitude"] = lats
        print(yem.head())
    except Exception as e:
        yem["adm" + str(adm)] = None
        print(e)

# reorder columns
yem = yem[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3", "longitude", "latitude"]]

# save as csv
yem.to_csv("../../files_for_db/geo/yem_geo.csv", index=False)

# save as shapefile
gdf = gpd.GeoDataFrame(
    yem,
    geometry = gpd.points_from_xy(
        x = yem.longitude,
        y = yem.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )
)
if not os.path.exists("../../files_for_db/shps/yem/"):
    os.mkdir("../../files_for_db/shps/yem/")
gdf.to_file("../../files_for_db/shps/yem/yem.shp", index = False)
shutil.make_archive("../../files_for_db/shps/yem", 'zip', "../../files_for_db/shps/yem")