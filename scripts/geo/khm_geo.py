import geopandas as gpd
import pandas as pd
import shutil
import os
from utils import *

# Fetch and read the datasets
DATA_PATH = str(os.path.abspath(os.path.join(__file__ ,"../../.."))) + "/data/KHM/"
schools2012 = gpd.read_file(DATA_PATH + "school_of_cambodia (2012)/school_of_cambodia.shp")
schools2014 = gpd.read_file(DATA_PATH + "Basic information of school (2014)/basic_information_of_school_2014.shp")
sec10_12 = gpd.read_file(DATA_PATH + "lycee-g10-12/Lycee G10-12.shp")
sec7_12 = gpd.read_file(DATA_PATH + "lycee-g7-12/Lycee G7-12.shp")

# Add dependency ID's to each dataset
# 2014 schools
deped_id_ls = ["basic_information_of_school_2014" + f".{idx}" for idx in range(1,schools2014.shape[0]+1)]
schools2014["deped_id"] = deped_id_ls

# 2012 schools
deped_id_ls = ["school_of_cambodia" + f".{idx}" for idx in range(1,schools2012.shape[0]+1)]
schools2012["deped_id"] = deped_id_ls

# Secondary schools 7-12
deped_id_ls = ["Lycee G7-12" + f".{idx}" for idx in range(1,sec7_12.shape[0]+1)]
sec7_12["deped_id"] = deped_id_ls

# Secondary schools 10-12
deped_id_ls = ["Lycee G10-12" + f".{idx}" for idx in range(1,sec10_12.shape[0]+1)]
sec10_12["deped_id"] = deped_id_ls

# Combine secondary schools
sec_schools = sec7_12.append(sec10_12, ignore_index=True)

# Update CRS and create lat/long for all schools

# Update CRS for 2014 schools
# info2014.crs
schools2014 = schools2014.set_crs("EPSG:32648") 
schools2014 = schools2014.to_crs("EPSG:4326")
# Create lat/long columns for 2014 schools
schools2014["longitude"] = schools2014.geometry.x
schools2014["latitude"] = schools2014.geometry.y

# Update CRS for 2012 schools
# schools2012.crs
schools2012 = schools2012.set_crs("EPSG:32648") 
schools2012 = schools2012.to_crs("EPSG:4326")
# # Create lat/long columns for 2012 schools
schools2012["longitude"] = schools2012.geometry.x
schools2012["latitude"] = schools2012.geometry.y

# Update CRS for secondary schools
# sec_schools.crs
sec_schools = sec_schools.set_crs("EPSG:32648") 
sec_schools = sec_schools.to_crs("EPSG:4326")
# Create lat/long columns for secondary schools
sec_schools["longitude"] = sec_schools.geometry.x
sec_schools["latitude"] = sec_schools.geometry.y

# Join all schools
schools2014 = schools2014[["PROVINCE","COMMUNE","DISTRICT","SCHOOL_NAM","VILLAGE","longitude","latitude","deped_id"]]
schools2012 = schools2012[["PROVINCE","COMMUNE","DISTRICT","SCHOOL_NAM","VILLAGE","longitude","latitude","deped_id"]]
sec_schools = sec_schools[["PROVINCE","COMMUNE","DISTRICT","SCHOOL_NAM","VILLAGE","longitude","latitude","deped_id"]]

khm_schools = schools2014.append(schools2012, ignore_index=True)
khm_schools = khm_schools.append(sec_schools, ignore_index=True)

# Generate GEO ID's
khm_schools['geo_id'] = pd.Series(range(0,len(khm_schools)+1)).apply(lambda x: 'KHM-{0:0>6}'.format(x))
# Add address variable
khm_schools["address"] = None
# Rename column names
khm_schools.rename(columns = {'SCHOOL_NAM':'school_name'}, inplace = True)

# Add ADM level variables
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

if not os.path.exists(PATH + "/files_for_db/shps/khm/"):
    os.mkdir(PATH + "/files_for_db/shps/khm/")

# Add shape file to files_for_db
gdf.to_file(PATH + "/files_for_db/shps/khm/khm.shp", index = False)

# Add zip file to files_for_db
shutil.make_archive(PATH + "/files_for_db/shps/khm", 'zip', PATH + "/files_for_db/shps/khm")