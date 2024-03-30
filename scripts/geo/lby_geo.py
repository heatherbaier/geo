import geopandas as gpd
import pandas as pd
import shutil
import os

from utils import *

# read in excel file
data = pd.read_excel("reach_lby_nationalschoolsassessment_complete_db_reliable__not_reliable_18oct2012.xlsx")

# only use reliable data
data = data[data["RELIABLE"] == "Reliable"]

# select necessary data and rename columns
data = data[["QI_eSchoolID", "QI_fSchoolName", "QII_4Street", "QII_5Longitude", "QII_6Latitude"]]
data.columns = ["deped_id", "school_name", "address", "latitude", "longitude"] # lat and long columns intentionally switched

# create geo ids
data.reset_index(inplace=True)
data["geo_id"] = data['index'].apply(lambda x: 'LBY-{0:0>6}'.format(x))

# create adm0
data["adm0"] = "LBY"

# add other adms
longs = data["longitude"].values
lats = data["latitude"].values
cols = ["index", "deped_id", "school_name", "address", "latitude", "longitude", "geo_id", "adm0"]
for adm in range(1, 4):
    try:
        cols += ["adm" + str(adm)]
        downloadGB("LBY", str(adm), ".")
        shp = gpd.read_file(getGBpath("LBY", f"ADM{str(adm)}", "."))
        data = gpd.GeoDataFrame(data, geometry = gpd.points_from_xy(data.longitude, data.latitude))
        
        data = data.set_crs("EPSG:4326")

        if adm == 1:
            data = gpd.clip(data, shp)
            longs = data["longitude"].values
            lats = data["latitude"].values
        
        data = gpd.tools.sjoin(data, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        data["longitude"] = longs
        data["latitude"] = lats
        print(data.head())
    except Exception as e:
        data["adm" + str(adm)] = None
        print(e)
        
# export as csv
data.to_csv("lby_geo.csv", index=False)

# export as shapefiles
gdf = gpd.GeoDataFrame(
    data,
    geometry = gpd.points_from_xy(
        x = data.longitude,
        y = data.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )
)
if not os.path.exists("../../files_for_db/shps/lby/"):
    os.mkdir("../../files_for_db/shps/lby/")
gdf.to_file("../../files_for_db/shps/lby/lby.shp", index = False)
shutil.make_archive("../../files_for_db/shps/lby", 'zip', "../../files_for_db/shps/lby")