import geopandas as gpd
import pandas as pd
import zipfile
import shutil
import os

from utils import *


df = gpd.read_file("../../data/BLZ/schools.geojson")
df = df[df["Sector"].isin(['Government Aided', 'Government', 'Govern+J617ment Aided'])]
df = df[df["Level_"].isin(['Primary', 'Preschool', 'Secondary', "Vocational"])]


df = df.rename(columns = {"Name": "school_name", "Code": "deped_id"})
df.columns = [i.lower() for i in df.columns]
df = df[["deped_id", "school_name", "longitude", "latitude", "address"]]
df = pd.DataFrame(df)
print(df.head())
print(df.shape)

iso = "BLZ"

df = df[df["longitude"] != 0]
df = df[df["latitude"] != 0]

# df = df.reset_index()
df['geo_id'] = ['BLZ-{0:0>6}'.format(i) for i in range(1, len(df) + 1)]


gdf = process_geo_file(
    df = df,
    iso=iso,
    gb_path="../../gb",
    # csv_out="/Users/heatherbaier/Documents/geo_git/files_for_db/geo/bhr_geo.csv",
    # shp_out="/Users/heatherbaier/Documents/geo_git/files_for_db/shps/bhr"
)
