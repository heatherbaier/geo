import geopandas as gpd
import pandas as pd
import shutil
import os
from utils import *

# Fetch and read the dataset
DATA_PATH = str(os.path.abspath(os.path.join(__file__ ,"../../.."))) + "/data/KEN/"
ken_schools = pd.read_csv(DATA_PATH + "/Kenya MOE Schools - Schools.csv")

# Subset the data
ken_schools = ken_schools[["Name", "Longitude", "Latitude"]]
# Rename columns
ken_schools.rename(columns = {'Name':'school_name', 'Longitude':'longitude', 'Latitude':'latitude'}, inplace = True)

# Generate GEO ID's
ken_schools['geo_id'] = pd.Series(range(0,len(ken_schools)+1)).apply(lambda x: 'KEN-{0:0>6}'.format(x))
# Add address variable
ken_schools["address"] = None

# Generate dependency ID's
deped_id_ls = ["Kenya MOE Schools - Schools" + f".{idx}" for idx in range(1,ken_schools.shape[0]+1)]
ken_schools["deped_id"] = deped_id_ls

# Add ADM level variables
longs = ken_schools["longitude"].values
lats = ken_schools["latitude"].values
cols = ["geo_id", "deped_id", "school_name", "address","adm0"]

# Add ADM0
ken_schools["adm0"] = "KEN"

# Add ADM1, ADM2, ADM3
for adm in range(1, 4):
    try:
        cols += ["adm" + str(adm)]
        downloadGB("KEN", str(adm), "../../gb")
        shp = gpd.read_file(getGBpath("KEN", f"ADM{str(adm)}", "../../gb"))
        ken_schools = gpd.GeoDataFrame(ken_schools, geometry = gpd.points_from_xy(ken_schools.longitude, ken_schools.latitude))
        ken_schools = gpd.tools.sjoin(ken_schools, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        ken_schools["longitude"] = longs
        ken_schools["latitude"] = lats
        print(ken_schools.head())

    except Exception as e:
        ken_schools["adm" + str(adm)] = None
        print(e)


PATH = str(os.path.abspath(os.path.join(__file__ ,"../../..")))

# Add KEN csv file to files_for_db
ken_schools.to_csv(PATH + "/files_for_db/geo/ken_geo.csv", index = False)

gdf = gpd.GeoDataFrame(
    ken_schools,
    geometry = gpd.points_from_xy(
        x = ken_schools.longitude,
        y = ken_schools.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )
)

if not os.path.exists(PATH + "/files_for_db/shps/ken/"):
    os.mkdir(PATH + "/files_for_db/shps/ken/")

# Add shape file to files_for_db
gdf.to_file(PATH + "/files_for_db/shps/ken/ken.shp", index = False)

# Add zip file to files_for_db
shutil.make_archive(PATH + "/files_for_db/shps/ken", 'zip', PATH + "/files_for_db/shps/ken")
