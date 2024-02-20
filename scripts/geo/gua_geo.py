import geopandas as gpd
import pandas as pd
import shutil
import os

from utils import *


# import all data
gua_1314 = pd.read_excel("../../data/GUA/establecimientos_2013-2014.xlsx")
gua_1516 = pd.read_excel("../../data/GUA/establecimientos_2015-2016.xlsx")
gua_1718 = pd.read_excel("../../data/GUA/establecimientos_2017-2018.xlsx")
gua_1920 = pd.read_excel("../../data/GUA/establecimientos_2019-2020.xlsx")
gua_2122 = pd.read_excel("../../data/GUA/establecimientos_2021-2022.xlsx")

# combine into one dataframe
gua_all = pd.concat([gua_1314, gua_1516, gua_1718, gua_1920, gua_2122])

# get rid of duplicates
gua_all.sort_values(by="Latitud", inplace=True)
gua_all.drop_duplicates(subset=["CodigoEst"], inplace=True)
gua_all.sort_values(by="CodigoEst", inplace=True)
gua_all.reset_index(inplace=True)

# select and rename relevant columns
gua_all = gua_all[["Departamento", "Municipio", "CodigoEst", "NombreEstablecimiento", "direccion", "Latitud", "Longitud"]]
gua_all.columns = ["adm1_temp", "adm2_temp", "deped_id", "school_name", "address", "latitude", "longitude"]

# create geo_ids
gua_all.reset_index(inplace=True)
gua_all["geo_id"] = gua_all['index'].apply(lambda x: 'GUA-{0:0>6}'.format(x))

# add adm0
gua_all["adm0"] = "GUA"

# add other adms
longs = gua_all["longitude"].values
lats = gua_all["latitude"].values
cols = ["index", "adm1_temp", "adm2_temp", "deped_id", "school_name", "address", "latitude", "longitude", "geo_id", "adm0"]
for adm in range(1, 4):
    try:
        cols += ["adm" + str(adm)]
        downloadGB("GTM", str(adm), ".")
        shp = gpd.read_file(getGBpath("GTM", f"ADM{str(adm)}", "."))
        gua_all = gpd.GeoDataFrame(gua_all, geometry = gpd.points_from_xy(gua_all.longitude, gua_all.latitude))
        gua_all = gpd.tools.sjoin(gua_all, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        gua_all["longitude"] = longs
        gua_all["latitude"] = lats
        print(gua_all.head())
    except Exception as e:
        gua_all["adm" + str(adm)] = None
        print(e)
        
# compare to adms in the dataset and use adms originally in dataset if no lat/long
gua_all["adm1"] = gua_all["adm1"].fillna((gua_all["adm1_temp"]).str.title())
gua_all["adm2"] = gua_all["adm2"].fillna((gua_all["adm2_temp"]).str.title())

# format other columns
gua_all["school_name"] = gua_all["school_name"].str.title()
gua_all["address"] = gua_all["address"].str.title()

# reorder final columns
gua_all = gua_all[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3", "longitude", "latitude"]]

# create csv
gua_all.to_csv("../../files_for_db/geo/gua_geo.csv", index=False)


# create shp files
gdf = gpd.GeoDataFrame(
    gua_all,
    geometry = gpd.points_from_xy(
        x = gua_all.longitude,
        y = gua_all.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )
)
if not os.path.exists("../../files_for_db/shps/gua/"):
    os.mkdir("../../files_for_db/shps/gua/")
gdf.to_file("../../files_for_db/shps/gua/gua.shp", index = False)
shutil.make_archive("../../files_for_db/shps/gua", 'zip', "../../files_for_db/shps/gua")
