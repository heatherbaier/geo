import geopandas as gpd
import pandas as pd
import zipfile
import shutil
import os

from utils import *


files = os.listdir("../../data/MEX/")
files = [i for i in files if "catalogo" in i]

dfs = []
for c, i in enumerate(files):
    cur = pd.read_csv(os.path.join("../../data/MEX/", i))
    cur = cur[["cv_cct", "c_nombre", "c_tipo", "c_estatus", "latitud", "longitud"]]
    cur = cur[cur["c_estatus"] == "ACTIVO"]
    cur = cur[cur["c_tipo"] == "ESCUELA"]
    dfs.append(cur)
    # print(cur.shape, c)
    print(c, end = "/r")


df = pd.concat(dfs)
df.columns = ["deped_id", "school_name", "c_tipo", "c_estatus", "latitude", "longitude"]
df = df.drop_duplicates(subset = ["deped_id"])
df = df[df["longitude"] != 0]
df = df[df["latitude"] != 0]
df = df.reset_index(drop=True)
df['geo_id'] = df.index.to_series().apply(lambda x: 'MEX-{0:0>6}'.format(x))

# df['geo_id'] = df['index'].apply(lambda x: 'MEX-{0:0>6}'.format(x))
df["adm0"] = "MEX"
df["address"] = None
df = df[["geo_id","deped_id","school_name","address","adm0", "longitude", "latitude"]]




# Geocode to ADM levels
iso = "MEX"
df["adm0"] = iso
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]


print(df.shape)
# --- FAST filter to ADM0 (replaces unary_union/within) ---
downloadGB(iso, "0", "../../gb")
adm0 = gpd.read_file(getGBpath(iso, "ADM0", "../../gb"))
df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs=adm0.crs)
# keep only points that fall inside ADM0 using spatial index
df = gpd.sjoin(df, adm0[["geometry"]], how="inner", predicate="within").drop(columns="index_right")
print(df.head())

# egae

print(df.shape)

print("Done with ADM0 clip.")


longs = df["longitude"].values
lats = df["latitude"].values


for adm in range(1, 4):
    print("ADM: ", adm)

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        df = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df.longitude, df.latitude))
        df = gpd.tools.sjoin(df, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        df["longitude"] = longs
        df["latitude"] = lats
        print(df.head())


    except Exception as e:

        df["adm" + str(adm)] = None
        print(e)

df = df[["geo_id","deped_id","school_name","address","adm0","adm1","adm2","adm3","longitude","latitude"]]

df.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/mex_geo.csv", index = False)

gdf = gpd.GeoDataFrame(
    df,
    geometry = gpd.points_from_xy(
        x = df.longitude,
        y = df.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/mex/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/mex/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/mex/mex.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/mex", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/mex")



    
print(df.head())
print(df.shape)


