import geopandas as gpd
import pandas as pd
import shutil
import os
from utils import *

# Fetch and read the datasets
DATA_PATH = str(os.path.abspath(os.path.join(__file__ ,"../../.."))) + "/data/KHM/"
khm_schools = gpd.read_file(DATA_PATH + "Basic information of school (2014)/basic_information_of_school_2014.shp")
khm_schools = khm_schools.to_crs("epsg:4326")


khm_schools["longitude"] = khm_schools.geometry.x
khm_schools["latitude"] = khm_schools.geometry.y
khm_schools = khm_schools[["SCHOOL_COD", "SCHOOL_NAM", "longitude", "latitude"]]
khm_schools.columns = ["deped_id", "school_name", "longitude", "latitude"]


print(khm_schools.head())


# # Generate GEO ID's
khm_schools['geo_id'] = pd.Series(range(0,len(khm_schools)+1)).apply(lambda x: 'KHM-{0:0>6}'.format(x))
# # Add address variable
khm_schools["address"] = None


# # Add ADM level variables
longs = khm_schools["longitude"].values
lats = khm_schools["latitude"].values
cols = ["geo_id", "deped_id", "school_name", "address","adm0"]

# Add ADM0
khm_schools["adm0"] = "KHM"

# Add ADM1, ADM2, ADM3
for adm in range(1, 4):
    try:
        cols += ["adm" + str(adm)]
        downloadGB("KHM", str(adm), "../../gb")
        shp = gpd.read_file(getGBpath("KHM", f"ADM{str(adm)}", "../../gb"))
        khm_schools = gpd.GeoDataFrame(khm_schools, geometry = gpd.points_from_xy(khm_schools.longitude, khm_schools.latitude))
        khm_schools = gpd.tools.sjoin(khm_schools, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        khm_schools["longitude"] = longs
        khm_schools["latitude"] = lats
        print(khm_schools.head())

    except Exception as e:
        khm_schools["adm" + str(adm)] = None
        print(e)

PATH = str(os.path.abspath(os.path.join(__file__ ,"../../..")))
# PATH = "/Users/paolagonzalez/Documents/Spring 2024/geolab/geo"

# Add KHM csv file to files_for_db
khm_schools.to_csv(PATH + "/files_for_db/geo/khm_geo.csv", index = False)

gdf = gpd.GeoDataFrame(
    khm_schools,
    geometry = gpd.points_from_xy(
        x = khm_schools.longitude,
        y = khm_schools.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )
)

print(khm_schools.head())

print(gdf.head())

if not os.path.exists(PATH + "/files_for_db/shps/khm/"):
    os.mkdir(PATH + "/files_for_db/shps/khm/")

# Add shape file to files_for_db
gdf.to_file(PATH + "/files_for_db/shps/khm/khm.shp", index = False)

# Add zip file to files_for_db
shutil.make_archive(PATH + "/files_for_db/shps/khm", 'zip', PATH + "/files_for_db/shps/khm")