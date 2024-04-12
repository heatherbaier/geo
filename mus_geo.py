import geopandas as gpd
import pandas as pd
import shutil
import os

from utils import *

# Clean coordinates
mus_ef = gpd.read_file('/Users/heatherbaier/Documents/geo_git/data/MUS/Locations of Secondary Schools in Mauritius_0.csv')
mus_ef = mus_ef[mus_ef['Longitude'] != 0]
mus_ef = mus_ef[mus_ef['Latitude'] != 0]


mus_ef = mus_ef.rename(columns = {'Latitude':'latitude','Longitude':'longitude'})

# Generate GEO ID's
mus_ef = mus_ef.reset_index()
mus_ef['geo_id'] = mus_ef['index'].apply(lambda x: 'MUS-{0:0>6}'.format(x))
mus_ef = mus_ef[["geo_id",'Name',"latitude", "longitude", "Address"]]
mus_ef['deped_id'] = None


longs = mus_ef["longitude"].values
lats = mus_ef["latitude"].values

# Geocode to ADM levels
iso = "MUS"
mus_ef["adm0"] = iso
cols = ["geo_id", "deped_id", "Name", "adm0", "Address"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), ".")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "."))
        mus_ef = gpd.GeoDataFrame(mus_ef, geometry = gpd.points_from_xy(mus_ef.longitude, mus_ef.latitude))
        mus_ef = gpd.tools.sjoin(mus_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        mus_ef["longitude"] = longs
        mus_ef["latitude"] = lats
        print(mus_ef.head())

    except Exception as e:

        mus_ef["adm" + str(adm)] = None
        print(e)

#renaming columns
mus_ef.columns = ["geo_id", "deped_id", "school_name", "adm0", "address", "adm1", "longitude","latitude","adm2","adm3"]

mus_ef = mus_ef[["geo_id","deped_id","school_name","address","adm0","adm1","adm2","adm3","longitude","latitude"]]

#Saving files
mus_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/mus_geo.csv", index = False)
gdf = gpd.GeoDataFrame(
    mus_ef,
    geometry = gpd.points_from_xy(
        x = mus_ef.longitude,
        y = mus_ef.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/mus/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/mus/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/mus/mus.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/mus", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/mus")