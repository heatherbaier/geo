import geopandas as gpd
import pandas as pd
import zipfile
import shutil
import os

from utils import *


base_dir = "../../data/CHL/directorios/"

files = os.listdir(base_dir)
files = [i for i in files if ".csv" in i]
files = [i for i in files if "Directorio" in i]
# sorted(files)
files


dfs, ids = [], []
for c, i in enumerate(files):
    df = pd.read_csv(os.path.join(base_dir, i), sep=";", decimal=",")
    df.columns = [i.lower() for i in df.columns]
    if "latitud" in df.columns:
        df = df.rename(columns = {"ïagno": "agno"})
        df = df[["agno", "rbd", "nom_rbd", "cod_depe2", "latitud", "longitud"]]
        if len(dfs) == 0:
            dfs.append(df)
        else:
            df = df[~df["rbd"].isin(ids)]
            print(df.shape, i)
            dfs.append(df)
        cur_ids = list(df["rbd"].unique())
        ids += cur_ids

all_schools = pd.concat(dfs)
all_schools.columns = [i.upper() for i in all_schools.columns]
all_schools["LATITUD"] = all_schools["LATITUD"].str.replace(",", ".")
all_schools["LONGITUD"] = all_schools["LONGITUD"].str.replace(",", ".")
all_schools = all_schools[all_schools["LATITUD"] != " "]
all_schools = all_schools[all_schools["LONGITUD"] != " "]
all_schools = all_schools.dropna(subset = ["LATITUD", "LONGITUD"]).sort_values(by = "RBD")
all_schools = all_schools[all_schools["COD_DEPE2"].isin([1,5])].rename(columns = {"RBD": "deped_id", "NOM_RBD": "school_name", "LATITUD": "latitude", "LONGITUD": "longitude"})

print(all_schools.shape)
print(all_schools["deped_id"].value_counts())
print(all_schools.head())
print(all_schools.tail())

all_schools = all_schools.reset_index(drop = True)
all_schools['geo_id'] = all_schools.index.to_series().apply(lambda x: 'CHL-{0:0>6}'.format(x))

# all_schools['geo_id'] = all_schools['index'].apply(lambda x: 'CHL-{0:0>6}'.format(x))
all_schools["adm0"] = "CHL"
all_schools["address"] = None

print(all_schools.columns)

all_schools = all_schools[["geo_id","deped_id","school_name","address","adm0", "longitude", "latitude"]]




# Geocode to ADM levels
iso = "CHL"
all_schools["adm0"] = iso
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]


print(all_schools.shape)
# --- FAST filter to ADM0 (replaces unary_union/within) ---
downloadGB(iso, "0", "../../gb")
adm0 = gpd.read_file(getGBpath(iso, "ADM0", "../../gb"))
all_schools = gpd.GeoDataFrame(all_schools, geometry=gpd.points_from_xy(all_schools.longitude, all_schools.latitude), crs=adm0.crs)
# keep only points that fall inside ADM0 using spatial index
all_schools = gpd.sjoin(all_schools, adm0[["geometry"]], how="inner", predicate="within").drop(columns="index_right")
print(all_schools.head())

# egae

print(all_schools.shape)

print("Done with ADM0 clip.")


longs = all_schools["longitude"].values
lats = all_schools["latitude"].values


for adm in range(1, 4):
    print("ADM: ", adm)

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        all_schools = gpd.GeoDataFrame(all_schools, geometry = gpd.points_from_xy(all_schools.longitude, all_schools.latitude))
        all_schools = gpd.tools.sjoin(all_schools, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        all_schools["longitude"] = longs
        all_schools["latitude"] = lats
        print(all_schools.head())


    except Exception as e:

        all_schools["adm" + str(adm)] = None
        print(e)

all_schools = all_schools[["geo_id","deped_id","school_name","address","adm0","adm1","adm2","adm3","longitude","latitude"]]

all_schools.to_csv("/Users/heatherbaier/Documents/geo/files_for_db/geo/chl_geo.csv", index = False)

gdf = gpd.GeoDataFrame(
    all_schools,
    geometry = gpd.points_from_xy(
        x = all_schools.longitude,
        y = all_schools.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo/files_for_db/shps/chl/"):
    os.mkdir("/Users/heatherbaier/Documents/geo/files_for_db/shps/chl/")

gdf.to_file("/Users/heatherbaier/Documents/geo/files_for_db/shps/chl/chl.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo/files_for_db/shps/chl", 'zip', "/Users/heatherbaier/Documents/geo/files_for_db/shps/chl")



    
print(all_schools.head())
print(all_schools.shape)


