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









# import pandas as pd

# tan_ef = pd.read_csv("../../data/TAN/pri-performing-all.csv")
# tan_ef = tan_ef[["CODE", "NAME", "LONGITUDE", "LATITUDE"]]
# tan_ef = tan_ef.drop_duplicates(subset = ["CODE"])
# tan_ef = tan_ef.reset_index()
# tan_ef['geo_id'] = tan_ef['index'].apply(lambda x: 'TAN-{0:0>6}'.format(x))
# tan_ef = tan_ef.drop(["index"], axis = 1)
# # tan_ef = tan_ef[["geo_id", "CODE", "NAME"]].rename(columns = {"CODE": "deped_id", "NAME": "school_name"})
# tan_ef = tan_ef[["geo_id", "CODE", "NAME", "LONGITUDE", "LATITUDE"]]
# tan_ef.columns = ["geo_id", "deped_id", "school_name", "longitude", "latitude"]
# print(tan_ef.head())

# # asga

# longs = tan_ef["longitude"].values
# lats = tan_ef["latitude"].values

# iso = "TZA"
# tan_ef["address"] = None
# tan_ef["adm0"] = iso

# # Geocode to ADM levels
# cols = ["geo_id", "deped_id", "school_name", "adm0", "address"]
# for adm in range(1, 4):

#     try:

#         cols += ["adm" + str(adm)]
#         downloadGB(iso, str(adm), "../../gb")
#         shp = gpd.read_file(getGBpath(iso, f"ADM{str(adm)}", "../../gb"))
#         tan_ef = gpd.GeoDataFrame(tan_ef, geometry = gpd.points_from_xy(tan_ef.longitude, tan_ef.latitude))
#         tan_ef = gpd.tools.sjoin(tan_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
#         tan_ef["longitude"] = longs
#         tan_ef["latitude"] = lats
#         print(tan_ef.head())


#     except Exception as e:

#         tan_ef["adm" + str(adm)] = None
#         print(e)

# tan_ef = tan_ef[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3", "longitude", "latitude"]]

# tan_ef.to_csv("/Users/heatherbaier/Documents/geo_git/files_for_db/geo/tan_geo.csv", index = False)


# gdf = gpd.GeoDataFrame(
#     tan_ef,
#     geometry = gpd.points_from_xy(
#         x = tan_ef.longitude,
#         y = tan_ef.latitude,
#         crs = 'EPSG:4326', # or: crs = pyproj.CRS.from_user_input(4326)
#     )

# )

# if not os.path.exists("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan/"):
#     os.mkdir("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan/")

# gdf.to_file("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan/tan.shp", index = False)

# shutil.make_archive("/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan", 'zip', "/Users/heatherbaier/Documents/geo_git/files_for_db/shps/tan")



# Tanzania merge stuff


import pandas as pd

# The coordinates only appear accuratein pri_performing
df = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/TAN/Consolidated_Primary_EnrolmentbyGrade_PTR_2022_PSLE2021.csv")
df = df[['REGION', 'COUNCIL', 'WARD', 'SCHOOL NAME', 'SCHOOL OWNERSHIP',
       'SCHOOL REG. NUMBER',
       'STD 1-BOYS', 'STD 1-GIRLS', 'STD 2-BOYS', 'STD 2-GIRLS', 'STD 3-BOYS',
       'STD 3-GIRLS', 'STD 4-BOYS', 'STD 4-GIRLS', 'STD 5-BOYS', 'STD 5-GIRLS',
       'STD 6-BOYS', 'STD 6-GIRLS', 'STD 7-BOYS', 'STD 7-GIRLS', 'TOTAL BOYS',
       'TOTAL GIRLS', 'ALL TEACHERS MALE', 'ALL TEACHERS FEMALE',
       'QUALIFIED TEACHERS MALE', 'QUALIFIED TEACHERS FEMALE', 'PTR', 'PQTR',
       'CLEAN CAND.S 2021', 'NUMBER OF CAND. PASSED (A-C)',
       'AVERAGE TOTAL MARKS (/300) 2021', 'AVERAGE TOTAL MARKS (/250) 2020',
       'CHANGE ON AVERAGE TOTAL MARKS FROM 2020', 'BAND OF SCHOOL 2021',
       'BAND OF SCHOOL 2020', 'RANK OF SCHOOL 2021', 'RANK OF SCHOOL 2020',
       'NO. OF PSLE CANDATES ']]
df.columns = [i.title() for i in df.columns]
df.head()
print(df.columns)

df2 = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/TAN/pri-performing-all.csv")
df2.columns = [i.title() for i in df2.columns]
df2["School Name"] = df2["Name"].str.split(" PR. ").str[0]
print(df2.columns)
print(df.shape)
df2["Ward"] = df2["Ward"].str.title()

df3 = pd.merge(df, df2, on = ["Ward", "School Name"])
print(df3.head())
print(df3.shape)


df3.to_csv("./test_merge1.csv")



df1 = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/TAN/Consolidated_Secondary_EnrolmentbyGrade_PTR_CSEE2021, 2022.csv")
df = df1[['Region', 'Council', 'Ward', 'School', 'Reg.No.',
       'NECTA Exam Centre No.', 'School Ownership',
       'Form 1-M', 'Form 1-F', 'Form 2-M', 'Form 2-F', 'Form 3-M', 'Form 3-F',
       'Form 4-M', 'Form 4-F', 'Form 5-M', 'Form 5-F', 'Form 6-M', 'Form 6-F',
       'M-Total', 'F-Total', 'Total Teachers-Male', 'Total Teachers-Female',
       'Qualified Teachers-Male', 'Qualified Teachers-Female', 'PTR', 'PQTR',
       'Regist. Cand. 2021', 'Clean Cand. 2021', 'Passed Cand. (I to IV) 2021',
       'Average GPA 2021', 'Band of School 2021', 'Band of School 2020',
       'Rank of School 2021', 'Rank of School 2020', 'Number of Candidates']]
df1 = df1.rename(columns = {"School": "School Name"})
df1.columns = [i.title() for i in df1.columns]
df1.head()
print(df1.columns)

df3 = pd.merge(df3, df1, on = ["Ward", "School Name"], how = "left")
print(df3.head())
print(df3.shape)

df3.to_csv("./test_merge2.csv")


# adgsa

tan_ef = df3

# old stuff



tan_ef = tan_ef[["School Reg. Number", "School Name", "Longitude_x", "Latitude_x"]]
tan_ef = tan_ef.drop_duplicates(subset = ["School Reg. Number"])
tan_ef = tan_ef.reset_index()
tan_ef['geo_id'] = tan_ef['index'].apply(lambda x: 'TAN-{0:0>6}'.format(x))
tan_ef = tan_ef.drop(["index"], axis = 1)
# tan_ef = tan_ef[["geo_id", "Code", "NAME"]].rename(columns = {"Code": "deped_id", "NAME": "school_name"})
tan_ef = tan_ef[["geo_id", "School Reg. Number", "School Name", "Longitude_x", "Latitude_x"]]
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



