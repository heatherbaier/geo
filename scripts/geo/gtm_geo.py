import geopandas as gpd
import pandas as pd
import shutil
import os

from utils import *


# import all data
gua_1314 = pd.read_excel("../../data/GTM/establecimientos_2013-2014.xlsx")
print("1")
gua_1516 = pd.read_excel("../../data/GTM/establecimientos_2015-2016.xlsx")
print("2")
gua_1718 = pd.read_excel("../../data/GTM/establecimientos_2017-2018.xlsx")
print("3")
gua_1920 = pd.read_excel("../../data/GTM/establecimientos_2019-2020.xlsx")
print("4")
gua_2122 = pd.read_excel("../../data/GTM/establecimientos_2021-2022.xlsx")
print("5")

# combine into one dataframe
gua_all = pd.concat([gua_1314, gua_1516, gua_1718, gua_1920, gua_2122])

gua_all = gua_all[gua_all["Sector"].isin(['OFICIAL', 'MUNICIPAL', 'COOPERATIVA'])]
gua_all = gua_all.drop_duplicates(subset = ["CodigoEst"])

# select and rename relevant columns
gua_all = gua_all[["CodigoEst", "NombreEstablecimiento", "direccion", "Latitud", "Longitud"]]
gua_all.columns = ["deped_id", "school_name", "address", "latitude", "longitude"]

gua_all = gua_all[gua_all["latitude"].notna()]
gua_all = gua_all[gua_all["longitude"].notna()]

gua_all = gua_all[gua_all["latitude"] != 0]
gua_all = gua_all[gua_all["longitude"] != 0]

iso = "GTM"

# df = df.reset_index()
gua_all['geo_id'] = ['GTM-{0:0>6}'.format(i) for i in range(1, len(gua_all) + 1)]

gdf = process_geo_file(
    df = gua_all,
    iso=iso,
    gb_path="../../gb",
    # csv_out="/Users/heatherbaier/Documents/geo_git/files_for_db/geo/bhr_geo.csv",
    # shp_out="/Users/heatherbaier/Documents/geo_git/files_for_db/shps/bhr"
)

