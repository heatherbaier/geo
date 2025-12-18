import geopandas as gpd
import pandas as pd
import shutil
import os

from utils import *


# Clean coordinates
bra_ef = pd.read_csv("../../data/BRA/Análise - Tabela da lista das escolas - Detalhado.csv")

# subset down to just main student "primary" schools of attendance and schools that just admit students with disabilities
types = ["ESCOLA ATENDE EXCLUSIVAMENTE ALUNOS COM DEFICIÊNCIA", "ESCOLA EM FUNCIONAMENTO E SEM RESTRIÇÃO DE ATENDIMENTO"]
bra_ef = bra_ef[bra_ef["Restrição de Atendimento"].isin(types)]
bra_ef = bra_ef[bra_ef["Dependência Administrativa"] != "Privada"]

bra_ef = bra_ef[["Escola", "Código INEP", "Latitude", "Longitude"]]
bra_ef.columns = ["school_name", "deped_id", "latitude", "longitude"]

bra_ef = bra_ef[bra_ef["longitude"] != "0"]
bra_ef = bra_ef[bra_ef["latitude"] != "0"]

# Force conversion, invalid strings become NaN
bra_ef["latitude"] = pd.to_numeric(bra_ef["latitude"], errors="coerce")
bra_ef["longitude"] = pd.to_numeric(bra_ef["longitude"], errors="coerce")

# Drop rows where coords are missing/invalid
bra_ef = bra_ef.dropna(subset=["latitude", "longitude"])


# fsgs


# Generate GEO ID's
bra_ef = bra_ef.reset_index()
bra_ef['oedc_id'] = bra_ef['index'].apply(lambda x: 'BRA-{0:0>6}'.format(x))
bra_ef = bra_ef[["oedc_id", "deped_id", "school_name", "latitude", "longitude"]]
bra_ef["address"] = None

print(bra_ef.head())

longs = bra_ef["longitude"].values
lats = bra_ef["latitude"].values

# Geocode to ADM levels
iso = "BRA"
bra_ef["adm0"] = iso
cols = ["oedc_id", "deped_id", "school_name", "adm0", "address"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        bra_ef = gpd.GeoDataFrame(bra_ef, geometry = gpd.points_from_xy(bra_ef.longitude, bra_ef.latitude))
        bra_ef = gpd.tools.sjoin(bra_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        bra_ef["longitude"] = longs
        bra_ef["latitude"] = lats
        print(bra_ef.head())

    except Exception as e:

        bra_ef["adm" + str(adm)] = None
        print(e)

bra_ef = bra_ef[["oedc_id","deped_id","school_name","address","adm0","adm1","adm2","adm3","longitude","latitude"]]

bra_ef.to_csv("../../files_for_db/geo/bra_geo.csv", index = False)

gdf = gpd.GeoDataFrame(
    bra_ef,
    geometry = gpd.points_from_xy(
        x = bra_ef.longitude,
        y = bra_ef.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("../../files_for_db/shps/bra/"):
    os.mkdir("../../files_for_db/shps/bra/")

gdf.to_file("../../files_for_db/shps/bra/bra.shp", index = False)

shutil.make_archive("../../files_for_db/shps/bra", 'zip', "../../files_for_db/shps/bra")