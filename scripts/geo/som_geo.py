import geopandas as gpd
import pandas as pd
import shutil
import os
from utils import *

# Fetch and read the datasets
DATA_PATH = str(os.path.abspath(os.path.join(__file__ ,"../../.."))) + "/data/SOM/Somalia - Education Facilities/"
som_schools = gpd.read_file(DATA_PATH + "Somalia - Education Facilities.shp")

# Subset and rename required columns
som_schools = som_schools[["NAMEOFSCHO","LATITUDE","LONGITUDE",]]
# Rename column names
som_schools.rename(columns = {'LONGITUDE':'longitude','LATITUDE':'latitude','NAMEOFSCHO':'school_name'}, inplace = True)

# Drop unknown schools
som_schools = som_schools.dropna()

# Add dependency ID's to each dataset
som_deped_id = ["Somalia - Education Facilities" + f".{idx}" for idx in range(1,som_schools.shape[0]+1)]
som_schools["deped_id"] = som_deped_id

# Add geo ID's
som_schools = som_schools.reset_index()
som_schools['geo_id'] = som_schools["index"].apply(lambda x: 'SOM-{0:0>6}'.format(x))
som_schools = som_schools.drop(["index"], axis = 1)

# Add address column 
som_schools["address"] = None

# Add ADM levels
som_schools["adm0"] = "SOM"
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]

longs = som_schools["longitude"].values
lats = som_schools["latitude"].values

# Add ADM1, ADM2, ADM3
for adm in range(1, 4):
    try:
        cols += ["adm" + str(adm)]
        downloadGB("SOM", str(adm), "../../gb")
        shp = gpd.read_file(getGBpath("SOM", f"ADM{str(adm)}", "../../gb"))
        shp = shp.set_crs("EPSG:4326")
        som_schools = gpd.GeoDataFrame(som_schools, geometry = gpd.points_from_xy(som_schools.longitude, som_schools.latitude))
        # Set CRS?
        som_schools = som_schools.set_crs("EPSG:4326")

        if adm == 1:
            som_schools = gpd.clip(som_schools, shp)
            longs = som_schools["longitude"].values
            lats = som_schools["latitude"].values

        som_schools = gpd.tools.sjoin(som_schools, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        som_schools["longitude"] = longs
        som_schools["latitude"] = lats
        print(som_schools.head())

    except Exception as e:
        som_schools["adm" + str(adm)] = None
        print("Error!")
        print(e)

som_schools = som_schools[["geo_id","deped_id","school_name","address","adm0","adm1","adm2","adm3","longitude","latitude"]]

# Add files
PATH = str(os.path.abspath(os.path.join(__file__ ,"../../..")))

# Add SOM csv file to files_for_db
som_schools.to_csv(PATH + "/files_for_db/geo/som_geo.csv", index = False)

gdf = gpd.GeoDataFrame(
    som_schools,
    geometry = gpd.points_from_xy(
        x = som_schools.longitude,
        y = som_schools.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )
)

if not os.path.exists(PATH + "/files_for_db/shps/som/"):
    os.mkdir(PATH + "/files_for_db/shps/som/")

# Add shape file to files_for_db
gdf.to_file(PATH + "/files_for_db/shps/som/som.shp", index = False)

# Add zip file to files_for_db
shutil.make_archive(PATH + "/files_for_db/shps/som", 'zip', PATH + "/files_for_db/shps/som")