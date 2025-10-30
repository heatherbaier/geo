import geopandas as gpd
import pandas as pd
import shutil
import os
from utils import *

# Fetch and read the datasets
DATA_PATH = str(os.path.abspath(os.path.join(__file__ ,"../../.."))) + "/data/KHM/"
khm_schools = gpd.read_file(DATA_PATH + "2014/Basic information of school (2014)/basic_information_of_school_2014.shp")
khm_schools = khm_schools.to_crs("epsg:4326")


khm_schools["longitude"] = khm_schools.geometry.x
khm_schools["latitude"] = khm_schools.geometry.y
khm_schools = khm_schools[["SCHOOL_COD", "SCHOOL_NAM", "longitude", "latitude"]]
khm_schools.columns = ["deped_id", "school_name", "longitude", "latitude"]
khm_schools["address"] = None


khm_schools = khm_schools.drop_duplicates(subset=["deped_id"], keep="first")

iso = "KHM"

# df = df.reset_index()
khm_schools['geo_id'] = ['KHM-{0:0>6}'.format(i) for i in range(1, len(khm_schools) + 1)]

gdf = process_geo_file(
    df = khm_schools,
    iso = iso,
    gb_path = "../../gb",
    # csv_out="/Users/heatherbaier/Documents/geo_git/files_for_db/geo/bhr_geo.csv",
    # shp_out="/Users/heatherbaier/Documents/geo_git/files_for_db/shps/bhr"
)