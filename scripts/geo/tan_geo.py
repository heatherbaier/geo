import geopandas as gpd
import pandas as pd
import zipfile
import shutil
import os

from utils import *

# #import and clean primary school data 
# tan_ef_prim = pd.read_csv("../../data/TAN/Consolidated_Primary_EnrolmentbyGrade_PTR_2022_PSLE2021.csv")

# tan_ef_prim = tan_ef_prim[tan_ef_prim["SCHOOL OWNERSHIP"] == "Government"]

# tan_ef_prim = tan_ef_prim[['SCHOOL REG. NUMBER', 'LATITUTE', 'LONGITUDE']]
# tan_ef_prim.columns = [_.title() for _ in tan_ef_prim]
# tan_ef_prim = tan_ef_prim.rename(columns = {"Latitute": "Latitude", "School Reg. Number": "deped_id"})

# #import and clean secondary school data
# tan_ef_sec = pd.read_csv("../../data/TAN/Consolidated_Secondary_EnrolmentbyGrade_PTR_CSEE2021, 2022.csv")
# tan_ef_sec = tan_ef_sec[['Reg.No.', 'Latitude', 'Longitude']]
# tan_ef_sec = tan_ef_sec.rename(columns = {"Reg.No.":"deped_id"})

# #put data together
# tan_ef = tan_ef_prim.append(tan_ef_sec)
# tan_ef = tan_ef.reset_index()

# #match with geo_ids
# tan_ids = pd.read_csv("tan_ids.csv")

# tan_ef = pd.merge(tan_ef, tan_ids, on="deped_id")

# tan_ef = tan_ef[["geo_id", "Longitude", "Latitude"]]
# tan_ef.columns = [_.lower() for _ in tan_ef.columns]

# #validate and export table
# print(tan_ef.head())

# tan_ef.to_csv("tan_coordinates.csv", index=False)


import pandas as pd

tan_ef = pd.read_csv("../../data/TAN/pri-performing-all.csv")
tan_ef = tan_ef[["CODE", "NAME", "LONGITUDE", "LATITUDE"]]
tan_ef = tan_ef.drop_duplicates(subset = ["CODE"])
tan_ef = tan_ef.reset_index()
tan_ef['geo_id'] = tan_ef['index'].apply(lambda x: 'TAN-{0:0>6}'.format(x))
tan_ef = tan_ef.drop(["index"], axis = 1)
# tan_ef = tan_ef[["geo_id", "CODE", "NAME"]].rename(columns = {"CODE": "deped_id", "NAME": "school_name"})
tan_ef = tan_ef[["geo_id", "CODE", "NAME", "LONGITUDE", "LATITUDE"]]
tan_ef.columns = ["geo_id", "deped_id", "school_name", "longitude", "latitude"]
print(tan_ef.head())

# asga

longs = tan_ef["longitude"].values
lats = tan_ef["latitude"].values

iso = "TZA"
tan_ef["address"] = None
tan_ef["adm0"] = iso

# Geocode to ADM levels
cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB(iso, str(adm), "../../gb")
        shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
        tan_ef = gpd.GeoDataFrame(tan_ef, geometry = gpd.points_from_xy(tan_ef.longitude, tan_ef.latitude))
        tan_ef = gpd.tools.sjoin(tan_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        tan_ef["longitude"] = longs
        tan_ef["latitude"] = lats
        print(tan_ef.head())


    except Exception as e:

        tan_ef["adm" + str(adm)] = None
        print(e)

tan_ef = tan_ef[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3", "longitude", "latitude"]]

tan_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/tan_geo.csv", index = False)


gdf = gpd.GeoDataFrame(
    tan_ef,
    geometry = gpd.points_from_xy(
        x = tan_ef.longitude,
        y = tan_ef.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan/tan.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan")




