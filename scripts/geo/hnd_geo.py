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

data = data.drop_duplicates(subset=["deped_id"], keep="first")

iso = "HND"

# df = df.reset_index()
data['geo_id'] = ['HND-{0:0>6}'.format(i) for i in range(1, len(data) + 1)]

gdf = process_geo_file(
    df = data,
    iso = iso,
    gb_path = "../../gb",
    # csv_out="/Users/heatherbaier/Documents/geo_git/files_for_db/geo/bhr_geo.csv",
    # shp_out="/Users/heatherbaier/Documents/geo_git/files_for_db/shps/bhr"
)