import geopandas as gpd
import pandas as pd
import shutil
import os
from utils import *

# Fetch and read the datasets
DATA_PATH = str(os.path.abspath(os.path.join(__file__ ,"../../.."))) + "/data/LAO/"
primary2014 = gpd.read_file(DATA_PATH + "lao_school_2014_primary/lao_school_2014_primary.shp")
schools2014 = gpd.read_file(DATA_PATH + "lao_school_info_2014/lao_school_info_2014.shp")

# Add dependency ID's to each dataset
# primary schools
deped_id_ls = ["school_2014_primary" + f".{idx}" for idx in range(1,primary2014.shape[0]+1)]
primary2014["deped_id"] = deped_id_ls

# schools
deped_id_ls = ["school_info_2014" + f".{idx}" for idx in range(1,schools2014.shape[0]+1)]
schools2014["deped_id"] = deped_id_ls


# Update CRS and create lat/long for all schools

# Update CRS for primary schools
# info2014.crs
primary2014 = primary2014.set_crs("EPSG:32648",allow_override=True) 
primary2014 = primary2014.to_crs("EPSG:4326")
# Create lat/long columns for primary schools
primary2014["longitude"] = primary2014.geometry.x
primary2014["latitude"] = primary2014.geometry.y

# Update CRS for 2014 schools
# schools2012.crs
schools2014 = primary2014.set_crs("EPSG:32648",allow_override=True) 
schools2014 = schools2014.to_crs("EPSG:4326")
# # Create lat/long columns for 2014 schools
schools2014["longitude"] = schools2014.geometry.x
schools2014["latitude"] = schools2014.geometry.y


# Join all schools
primary2014 = primary2014[["School_Cod","Facility_N","Disctrict_","Provinc_ c","Longitude","Latitude"]]
schools2014 = schools2014[["School_Cod","Facility_N","Disctrict_","Provinc_ c","Longitude","Latitude"]]


lao_schools = pd.concat([primary2014, schools2014], ignore_index=True)


# Generate GEO ID's
lao_schools['geo_id'] = pd.Series(range(0,len(lao_schools)+1)).apply(lambda x: 'LAO-{0:0>6}'.format(x))
# Add address variable
lao_schools["address"] = None
# Rename column names
lao_schools.rename(columns = {'School_Cod':'deped_id','Facility_N':'school_name','Longitude':'longitude', 'Latitude':'latitude'}, inplace = True)

# Add ADM level variables
longs = lao_schools["longitude"].values
lats = lao_schools["latitude"].values
cols = ["geo_id", "deped_id", "school_name", "address","adm0"]

# Add ADM0
lao_schools["adm0"] = "LAO"

# Add ADM1, ADM2, ADM3
for adm in range(1, 4):
    try:
        cols += ["adm" + str(adm)]
        downloadGB("LAO", str(adm), "../../gb")
        shp = gpd.read_file(getGBpath("LAO", f"ADM{str(adm)}", "../../gb"))
        lao_schools = gpd.GeoDataFrame(lao_schools, geometry = gpd.points_from_xy(lao_schools.longitude, lao_schools.latitude))
        lao_schools = gpd.tools.sjoin(lao_schools, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        lao_schools["longitude"] = longs
        lao_schools["latitude"] = lats
        print(lao_schools.head())

    except Exception as e:
        lao_schools["adm" + str(adm)] = None
        print(e)

PATH = str(os.path.abspath(os.path.join(__file__ ,"../../..")))

# Add LAO csv file to files_for_db
lao_schools.to_csv(PATH + "/files_for_db/geo/lao_geo.csv", index = False)

gdf = gpd.GeoDataFrame(
    lao_schools,
    geometry = gpd.points_from_xy(
        x = lao_schools.longitude,
        y = lao_schools.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )
)

if not os.path.exists(PATH + "/files_for_db/shps/lao/"):
    os.mkdir(PATH + "/files_for_db/shps/lao/")

# Add shape file to files_for_db
gdf.to_file(PATH + "/files_for_db/shps/lao/lao.shp", index = False)

# Add zip file to files_for_db
shutil.make_archive(PATH + "/files_for_db/shps/lao", 'zip', PATH + "/files_for_db/shps/lao")