import geopandas as gpd
import pandas as pd
import shutil
import os

from utils import *


geo = pd.read_csv("../../files_for_db/geo/gtm_geo.csv")

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
gua_all = gua_all[gua_all["Nivel"] != 'PRIMARIA DE ADULTOS']

level_map = {
    "INICIAL": "pre_primary",         # ISCED 0
    "PREPRIMARIA": "pre_primary",     # ISCED 0
    "PRIMARIA": "primary",           # ISCED 1
    "BASICO": "lower_secondary",     # ISCED 2
    "DIVERSIFICADO": "upper_secondary", # ISCED 3
}

gua_all["school_level"] = gua_all["Nivel"].str.strip().str.upper().map(level_map)
gua_all["is_cooperative"] = gua_all["Sector"].str.strip().str.upper().eq("COOPERATIVA")

gua_all = gua_all.rename(columns = {"CodigoEst": "deped_id"})
gua_all = gua_all[["deped_id", 'school_level', 'is_cooperative']]
t = pd.merge(geo, gua_all, on = "deped_id")[["geo_id", "deped_id", "school_level", "is_cooperative"]]

t.to_csv("../../files_for_db_level/gtm_level.csv", index = False)

