import geopandas as gpd
import pandas as pd
import shutil
import os

from utils import *

# import shapefile
gdf = gpd.read_file("../../data/PNG/png_edup_2000_nso_edit/png_edup_2000_nso_edit.shp")

# use multipoint to get lat and long
gdf["point"] = gdf.centroid
gdf["longitude"] = gdf.point.x
gdf["latitude"] = gdf.point.y

# select and rename columns
gdf = gdf[["ADM1_NAME", "ADM2_NAME", "ADM3_NAME", "EDU_NAME", "longitude", "latitude"]]
gdf.columns = ["adm1", "adm2", "adm3", "school_name", "longitude", "latitude"]

# create missing columns
gdf["adm0"] = "PNG"
gdf["deped_id"] = None
gdf["address"] = None

# change from all caps to title case
for column in ["adm1", "adm2", "adm3", "school_name"]:
    gdf[column] = gdf[column].str.title()
    
# create geo ids
gdf.reset_index(inplace=True)
gdf["geo_id"] = gdf['index'].apply(lambda x: 'PNG-{0:0>6}'.format(x))

# select and reorder final columns
gdf = gdf[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3", "longitude", "latitude"]]

# export as csv
gdf.to_csv("../../files_for_db/geo/png_geo.csv", index=False)

# export as shapefile
gdf = gpd.GeoDataFrame(
    gdf,
    geometry = gpd.points_from_xy(
        x = gdf.longitude,
        y = gdf.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )
)
if not os.path.exists("../../files_for_db/shps/png/"):
    os.mkdir("../../files_for_db/shps/png/")
gdf.to_file("../../files_for_db/shps/png/png.shp", index = False)
shutil.make_archive("../../files_for_db/shps/png", 'zip', "../../files_for_db/shps/png")