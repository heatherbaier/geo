import geopandas as gpd
import pandas as pd
import shutil
import os
from utils import *

# Fetch and read the datasets
DATA_PATH = str(os.path.abspath(os.path.join(__file__ ,"../../.."))) + "/data/ZWE/"
zwe1 = pd.read_excel(DATA_PATH + "schoolsandtheircoordinates2020.xlsx")
zwe1 = zwe1[['Name','latitude', 'longitude']]

# Add dependency ID's to each dataset
# 2014 schools
deped_id_ls = ["schoolsandtheircoordinates2020" + f".{idx}" for idx in range(1,zwe1.shape[0]+1)]
zwe1["deped_id"] = deped_id_ls

# Generate GEO ID's
zwe1['geo_id'] = pd.Series(range(0,len(zwe1)+1)).apply(lambda x: 'ZWE-{0:0>6}'.format(x))
# Add address and adm0 variable
zwe1["address"] = None
zwe1["adm0"] = "ZWE"
# Rename column names
zwe1.rename(columns = {'Name':'school_name'}, inplace = True) 

# Remove schools with no lat/long coordinates
no_lat = zwe1['latitude']=='(blank)'
no_long = zwe1['longitude']=='(blank)'
zwe1 = zwe1[~no_lat]
zwe1 = zwe1[~no_long]
zwe1 = zwe1.reset_index(drop=True)

# Create ADM levels
longs = zwe1["longitude"].values
lats = zwe1["latitude"].values
cols = ["geo_id", "deped_id", "school_name", "address","adm0"]
for adm in range(1, 4):
    try:
        cols += ["adm" + str(adm)]
        downloadGB("ZWE", str(adm), "../../gb")
        shp = gpd.read_file(getGBpath("ZWE", f"ADM{str(adm)}", "../../gb"))
        zwe1 = gpd.GeoDataFrame(zwe1, geometry = gpd.points_from_xy(zwe1.longitude, zwe1.latitude))
        zwe1 = gpd.tools.sjoin(zwe1, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        zwe1["longitude"] = longs
        zwe1["latitude"] = lats
        print(zwe1.head())

    except Exception as e:

        zwe1["adm" + str(adm)] = None
        print(e)


zwe1 = zwe1[["geo_id","deped_id","school_name","address","adm0","adm1","adm2","adm3","longitude","latitude"]]

PATH = str(os.path.abspath(os.path.join(__file__ ,"../../..")))

 # Add BGD csv file to files_for_db
zwe1.to_csv(PATH + "/files_for_db/geo/zwe_geo.csv", index = False)

gdf = gpd.GeoDataFrame(
    zwe1,
    geometry = gpd.points_from_xy(
        x = zwe1.longitude,
        y = zwe1.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )
)

if not os.path.exists(PATH + "/files_for_db/shps/zwe/"):
    os.mkdir(PATH + "/files_for_db/shps/zwe/")

# Add shape file to files_for_db
gdf.to_file(PATH + "/files_for_db/shps/zwe/zwe.shp", index = False)

# Add zip file to files_for_db
shutil.make_archive(PATH + "/files_for_db/shps/zwe", 'zip', PATH + "/files_for_db/shps/zwe")