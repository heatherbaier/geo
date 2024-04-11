import geopandas as gpd
import pandas as pd
import shutil
import os

from utils import *

# import data
data = pd.read_excel("../../data/HND/coordenadasporcentroeducativo_siplie_23marzo2020.xlsx", header=6)

# fix null coordinates
data["Latitud"] = data["Latitud"].apply(lambda x: None if x<0.1 else x)
data["Longitud"] = data["Longitud"].apply(lambda x: None if x<-90 else x)

# select and rename columns
data = data[["Departamento", "Municipio", "CodigoCentro", "NombreCentro", "DireccionCentro", "Latitud", "Longitud"]]
data.columns = ["adm1_temp", "adm2_temp", "deped_id", "school_name", "address", "latitude", "longitude"]

# create geo_ids
data.reset_index(inplace=True)
data["geo_id"] = data['index'].apply(lambda x: 'HND-{0:0>6}'.format(x))

# create adm0
data["adm0"] = "HND"

# add other adms
longs = data["longitude"].values
lats = data["latitude"].values
cols = ["index", "adm1_temp", "adm2_temp", "deped_id", "school_name", "address", "latitude", "longitude", "geo_id", "adm0"]
for adm in range(1, 4):
    try:
        cols += ["adm" + str(adm)]
        downloadGB("HND", str(adm), ".")
        shp = gpd.read_file(getGBpath("HND", f"ADM{str(adm)}", "."))
        shp = shp.set_crs("EPSG:4326")
        data = gpd.GeoDataFrame(data, geometry = gpd.points_from_xy(data.longitude, data.latitude))

        data = data.set_crs("EPSG:4326")
        shp = shp.set_crs("EPSG:4326")

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

# compare to adms in the dataset and use adms originally in dataset if no lat/long
data["adm1"] = data["adm1"].fillna((data["adm1_temp"]).str.title())
data["adm2"] = data["adm2"].fillna((data["adm2_temp"]).str.title())

# reformat columns
data["school_name"] = data["school_name"].str.title()
data["address"] = data["address"].str.title()

# select and reorder columns
data = data[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3", "longitude", "latitude"]]

# export as csv
data.to_csv("../../files_for_db/geo/hnd_geo.csv", index=False)

# create shp files
gdf = gpd.GeoDataFrame(
    data,
    geometry = gpd.points_from_xy(
        x = data.longitude,
        y = data.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )
)
if not os.path.exists("../../files_for_db/shps/hnd/"):
    os.mkdir("../../files_for_db/shps/hnd/")
gdf.to_file("../../files_for_db/shps/hnd/hnd.shp", index = False)
shutil.make_archive("../../files_for_db/shps/hnd", 'zip', "../../files_for_db/shps/hnd")