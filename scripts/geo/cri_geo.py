import geopandas as gpd
import pandas as pd
import shutil
import os

from utils import *


cri_ef = gpd.read_file("/Users/heatherbaier/Documents/geo_git/data/CRI/cri_schools/CE_PUBLICOS_SABER_JUN24_wsg4326.shp")
cri_ef["CODSABER"] = cri_ef["CODSABER"].astype(str).str.split("-").str[0]
cri_ef.head()

import pandas as pd
import re
import unicodedata

# --- CONFIG ---
excel_path = "/Users/heatherbaier/Documents/geo_git/data/CRI/REPITENTES_EN_ESCUELAS_2014-2022.xlsx"
sheet_name = 0            # or the sheet name string
header_rows = [0, 1, 2]   # the three header rows

# --- helpers ---
def normalize_text(s: str) -> str:
    # strip, lowercase, remove accents, collapse spaces/punct to underscores
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w]+", "_", s)    # non-word chars -> underscore
    s = re.sub(r"_+", "_", s).strip("_")
    return s

def flatten_cols(cols):
    """cols is a tuple from the MultiIndex; keep non-empty parts only."""
    parts = [str(p) for p in cols if pd.notna(p) and str(p).strip() and str(p).strip() != "-"]
    if not parts:
        return "unnamed"
    return normalize_text("_".join(parts))

def dedupe(names):
    """ensure column names are unique by appending suffixes"""
    seen = {}
    out = []
    for n in names:
        if n not in seen:
            seen[n] = 0
            out.append(n)
        else:
            seen[n] += 1
            out.append(f"{n}_{seen[n]}")
    return out

# --- read as MultiIndex columns ---
df = pd.read_excel(excel_path, sheet_name=sheet_name, header=header_rows)

# If some top-level header cells were merged/blank, pandas will put NaN in those slots.
# The flatten function above ignores NaNs and "-" placeholders automatically.

# --- flatten to single row of headers ---
new_cols = [flatten_cols(c) if isinstance(c, tuple) else flatten_cols((c,)) for c in df.columns]
new_cols = dedupe(new_cols)  # make sure names are unique
df.columns = new_cols

col_map = {"estudiantes_repitentes_en_i_y_ii_ciclos_2014_2022_nota_no_incluye_los_datos_del_curso_lectivo_2017_codigo": "codigo",
           "estudiantes_repitentes_en_i_y_ii_ciclos_2014_2022_nota_no_incluye_los_datos_del_curso_lectivo_2017_region": "region",
           "estudiantes_repitentes_en_i_y_ii_ciclos_2014_2022_nota_no_incluye_los_datos_del_curso_lectivo_2017_curso_lectivo": "year",
           "estudiantes_repitentes_en_i_y_ii_ciclos_2014_2022_nota_no_incluye_los_datos_del_curso_lectivo_2017_nombre": "school_name",
           "estudiantes_repitentes_en_i_y_ii_ciclos_2014_2022_nota_no_incluye_los_datos_del_curso_lectivo_2017_provincia": "province",
           "estudiantes_repitentes_en_i_y_ii_ciclos_2014_2022_nota_no_incluye_los_datos_del_curso_lectivo_2017_cires": "cires",
           "estudiantes_repitentes_en_i_y_ii_ciclos_2014_2022_nota_no_incluye_los_datos_del_curso_lectivo_2017_canton": "canton",
           "estudiantes_repitentes_en_i_y_ii_ciclos_2014_2022_nota_no_incluye_los_datos_del_curso_lectivo_2017_distrito": "distrito",
           "estudiantes_repitentes_en_i_y_ii_ciclos_2014_2022_nota_no_incluye_los_datos_del_curso_lectivo_2017_poblado": "poblado"}

df.rename(columns=col_map, inplace=True)

df["codigo"] = "10" + df["codigo"].astype(str)
import unicodedata

cri_ef["PROVINCIA"] = cri_ef["PROVINCIA"].astype(str).apply(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8'))
cri_ef["CANTON"] = cri_ef["CANTON"].astype(str).apply(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8'))
cri_ef["DISTRITO"] = cri_ef["DISTRITO"].astype(str).apply(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8'))
cri_ef["CENTRO_EDU"] = cri_ef["CENTRO_EDU"].astype(str).apply(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8'))


df["province"] = df["province"].astype(str).apply(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8'))
df["canton"] = df["canton"].astype(str).apply(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8'))
df["distrito"] = df["distrito"].astype(str).apply(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8'))
df["school_name"] = df["school_name"].astype(str).apply(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8'))


df["canton"] = df["canton"].replace(["LEON CORTES CASTRO", "LEON CORTES"], "LEON CORTES")
df["canton"] = df["canton"].replace(["LEON CORTES CASTRO", "LEON CORTES"], "LEON CORTES")

# df["distrito"] = df["distrito"].str.replace(["AGUA CALIENTE O SAN FRANCISO"], "AGUACALIENTE O SAN FRANCISCO")
# df["distrito"] = df["distrito"].str.replace("", "AGUA CALIENTE O SAN FRANCISO")
df["distrito"] = df["distrito"].str.replace("AGUABUENA", "AGUA BUENA")
df["distrito"] = df["distrito"].replace(
    ["AGUA CALIENTE", "AGUA CALIENTE O SAN FRANCISO"], 
    "AGUACALIENTE O SAN FRANCISO"
)

df_y = df[df["year"] == 2016].copy()
df_y["region"] = "DIRECCIÓN REGIONAL " + df_y["region"].astype(str)

test2 = pd.merge(cri_ef.drop(["OBJECTID", "TIPO_INSTI", "ESTADO"], axis = 1), df_y[list(col_map.values())], left_on=["CENTRO_EDU", "REGIONAL", "PROVINCIA", "CANTON", "DISTRITO", "POBLADO"], right_on=["school_name", "region", "province", "canton", "distrito", "poblado"], how="inner")
print(test2.shape)


test2 = test2.rename(columns = {"CODSABER": "deped_id"})

test2["longitude"] = test2.geometry.x
test2["latitude"] = test2.geometry.y

test2 = test2[test2["longitude"] != 0]
test2 = test2[test2["latitude"] != 0]


test2 = test2[["deped_id", "school_name", "longitude", "latitude"]]


cri_ef = test2

# Generate GEO ID's
cri_ef = cri_ef.reset_index()
cri_ef['geo_id'] = cri_ef['index'].apply(lambda x: 'CRI-{0:0>6}'.format(x))
cri_ef = cri_ef[["geo_id", "deped_id", "school_name", "latitude", "longitude"]].rename(columns = {"gml_id": "deped_id"})
cri_ef["address"] = None


print(cri_ef.head())


longs = cri_ef["longitude"].values
lats = cri_ef["latitude"].values

# Geocode to ADM levels
iso = "CRI"
cri_ef["adm0"] = iso
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        cri_ef = gpd.GeoDataFrame(cri_ef, geometry = gpd.points_from_xy(cri_ef.longitude, cri_ef.latitude))
        cri_ef = gpd.tools.sjoin(cri_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        cri_ef["longitude"] = longs
        cri_ef["latitude"] = lats
        print(cri_ef.head())


    except Exception as e:

        cri_ef["adm" + str(adm)] = None
        print(e)

cri_ef = cri_ef[["geo_id","deped_id","school_name","address","adm0","adm1","adm2","adm3","longitude","latitude"]]

cri_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/cri_geo.csv", index = False)

gdf = gpd.GeoDataFrame(
    cri_ef,
    geometry = gpd.points_from_xy(
        x = cri_ef.longitude,
        y = cri_ef.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/cri/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/cri/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/cri/cri.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/cri", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/cri")


# import geopandas as gpd
# import pandas as pd
# import shutil
# import os

# from utils import *


# # Clean coordinates
# cri_ef = gpd.read_file("/Users/heatherbaier/Documents/geo_git/data/CRI/cri_schools/CE_PUBLICOS_SABER_JUN24.shp")

# print(cri_ef.columns)

# sagsa

# cri_ef = cri_ef[["gml_id", "ESTABLECIM", "POINT_X", "POINT_Y"]]
# cri_ef.columns = ["deped_id", "school_name", "longitude", "latitude"]
# cri_ef = cri_ef[cri_ef["longitude"] != 0]
# cri_ef = cri_ef[cri_ef["latitude"] != 0]


# # Generate GEO ID's
# cri_ef = cri_ef.reset_index()
# cri_ef['geo_id'] = cri_ef['index'].apply(lambda x: 'cri-{0:0>6}'.format(x))
# cri_ef = cri_ef[["geo_id", "deped_id", "school_name", "latitude", "longitude"]].rename(columns = {"gml_id": "deped_id"})
# cri_ef["address"] = None

# print(cri_ef.head())

# longs = cri_ef["longitude"].values
# lats = cri_ef["latitude"].values

# # Geocode to ADM levels
# iso = "cri"
# cri_ef["adm0"] = iso
# cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
# for adm in range(1, 4):

#     try:

#         cols += ["adm" + str(adm)]
#         downloadGB(iso, str(adm), "../../gb")
#         shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
#         cri_ef = gpd.GeoDataFrame(cri_ef, geometry = gpd.points_from_xy(cri_ef.longitude, cri_ef.latitude))
#         cri_ef = gpd.tools.sjoin(cri_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
#         cri_ef["longitude"] = longs
#         cri_ef["latitude"] = lats
#         print(cri_ef.head())


#     except Exception as e:

#         cri_ef["adm" + str(adm)] = None
#         print(e)

# cri_ef = cri_ef[["geo_id","deped_id","school_name","address","adm0","adm1","adm2","adm3","longitude","latitude"]]

# cri_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/cri_geo.csv", index = False)

# gdf = gpd.GeoDataFrame(
#     cri_ef,
#     geometry = gpd.points_from_xy(
#         x = cri_ef.longitude,
#         y = cri_ef.latitude,
#         crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
#     )

# )

# if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/cri/"):
#     os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/cri/")

# gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/cri/cri.shp", index = False)

# shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/cri", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/cri")