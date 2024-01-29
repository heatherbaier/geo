import geopandas as gpd
import pandas as pd
import zipfile
import shutil
import os

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


tan = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/TAN/pri-performing-all.csv")
tan = tan[["CODE", "NAME", "REGION", "DISTRICT", "WARD", "OWNERSHIP", "LONGITUDE", "LATITUDE"]]
tan = tan.rename(columns = {"CODE": "deped_id"})

ids = pd.read_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/ids/tan_ids.csv")

tan = pd.merge(ids, tan, on = "deped_id")

tan = tan[["geo_id", "LONGITUDE", "LATITUDE"]]
tan.columns = ["geo_id", "longitude", "latitude"]

tan.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/coordinates/tan_coordinates.csv", index=False)

gdf = gpd.GeoDataFrame(
    tan,
    geometry = gpd.points_from_xy(
        x = tan.longitude,
        y = tan.latitude,
        crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
    )

)

if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan/"):
    os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan/")

gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan/tan.shp", index = False)

shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan")

# zf = zipfile.ZipFile("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan.zip", "w")
# # for files in os.listdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/"):
# for filename in os.listdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan/"):
#     zf.write(os.path.join("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan/", filename))
# zf.close()


# with zipfile.ZipFile("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan.zip", 'w') as myzip:
#     myzip.write("/Users/heatherbaier/Documents/geo_git/files_for_db/coordinates/tan_coordinates.csv")

print(tan.head())
print(gdf.head())
