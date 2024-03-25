import geopandas as gpd
import pandas as pd
import shutil
import os
from utils import *

# Fetch and read the datasets
DATA_PATH = str(os.path.abspath(os.path.join(__file__ ,"../../.."))) + "/data/BGD/bgd_poi_educationfacilities_lged/"
bgd1 = gpd.read_file(DATA_PATH + "bgd_poi_educationfacilities_lged.shp")
# bgd2 = gpd.read_file(DATA_PATH + "IDN_school_facilities.shp")
# bgd3 = gpd.read_file(DATA_PATH + "kgz_edufac_unicef.shp")

# Subset and rename the required variables
bgd1 = bgd1[["X_LOC","Y_LOC","SCH_NAME","SCH_B_ADDR"]]
# Rename column names
bgd1.rename(columns = {'X_LOC':'longitude','Y_LOC':'latitude','SCH_NAME':'school_name','SCH_B_ADDR':'address'}, inplace = True)

# bgd2 = bgd2[["NAME","ADDRESS","Longitude","Latitude"]]
# Rename column names
# bgd2.rename(columns = {'Longitude':'longitude','Latitude':'latitude','NAME':'school_name','ADDRESS':'address'}, inplace = True)

# bgd3 = bgd3[["school_nam","school_loc","Longitude","Latitude"]]
# Rename column names
# bgd3.rename(columns = {'Longitude':'longitude','Latitude':'latitude','school_nam':'school_name','school_loc':'address'}, inplace = True)

# Add dependency ID's to each dataset
bgd1_deped_id = ["bgd_poi_educationfacilities_lged" + f".{idx}" for idx in range(1,bgd1.shape[0]+1)]
bgd1["deped_id"] = bgd1_deped_id

# bgd2_deped_id = ["IDN_school_facilities" + f".{idx}" for idx in range(1,bgd2.shape[0]+1)]
# bgd2["deped_id"] = bgd2_deped_id
#
# bgd3_deped_id = ["kgz_edufac_unicef" + f".{idx}" for idx in range(1,bgd3.shape[0]+1)]
# bgd3["deped_id"] = bgd3_deped_id

# Combine the schools
bgd_schools = bgd1#.append(bgd2, ignore_index=True)
# bgd_schools = bgd_schools.append(bgd3, ignore_index=True)
# Drop duplicated schools
bgd_schools = bgd_schools.drop_duplicates(subset=['longitude','latitude'])

print("SHAPE: ", bgd_schools.shape)
bgd_schools = bgd_schools[bgd_schools["latitude"] != 0]
bgd_schools = bgd_schools[bgd_schools["longitude"] != 0]
print("SHAPE: ", bgd_schools.shape)


# Add ADM level variables
longs = bgd_schools["longitude"].values
lats = bgd_schools["latitude"].values
cols = ["geo_id", "deped_id", "school_name", "address","adm0"]

# Add ADM0
bgd_schools["adm0"] = "BGD"


bgd_schools = bgd_schools.reset_index()
bgd_schools['geo_id'] = bgd_schools['index'].apply(lambda x: 'BGD-{0:0>6}'.format(x))
bgd_schools = bgd_schools.drop(["index"], axis = 1)


print(bgd_schools)


# Add ADM1, ADM2, ADM3
for adm in range(1, 4):
    try:
        cols += ["adm" + str(adm)]
        downloadGB("BGD", str(adm), "../../gb")
        shp = gpd.read_file(getGBpath("BGD", f"ADM{str(adm)}", "../../gb"))
        shp = shp.set_crs("EPSG:4326")
        bgd_schools = gpd.GeoDataFrame(bgd_schools, geometry = gpd.points_from_xy(bgd_schools.longitude, bgd_schools.latitude))
        # Set CRS?
        bgd_schools = bgd_schools.set_crs("EPSG:4326")

        if adm == 1:
            bgd_schools = gpd.clip(bgd_schools, shp)
            longs = bgd_schools["longitude"].values
            lats = bgd_schools["latitude"].values

        bgd_schools = gpd.tools.sjoin(bgd_schools, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        bgd_schools["longitude"] = longs
        bgd_schools["latitude"] = lats
        print(bgd_schools.head())

    except Exception as e:
        bgd_schools["adm" + str(adm)] = None
        print("Error!")
        print(e)



bgd_schools = bgd_schools[["geo_id","deped_id","school_name","address","adm0","adm1","adm2","adm3","longitude","latitude"]]

PATH = str(os.path.abspath(os.path.join(__file__ ,"../../..")))

# Add BGD csv file to files_for_db
bgd_schools.to_csv(PATH + "/files_for_db/geo/bgd_geo.csv", index = False)

gdf = gpd.GeoDataFrame(
    bgd_schools,
    geometry = gpd.points_from_xy(
        x = bgd_schools.longitude,
        y = bgd_schools.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )
)

if not os.path.exists(PATH + "/files_for_db/shps/bgd/"):
    os.mkdir(PATH + "/files_for_db/shps/bgd/")

# Add shape file to files_for_db
gdf.to_file(PATH + "/files_for_db/shps/bgd/bgd.shp", index = False)

# Add zip file to files_for_db
shutil.make_archive(PATH + "/files_for_db/shps/bgd", 'zip', PATH + "/files_for_db/shps/bgd")