import geopandas as gpd
import pandas as pd
import shutil
import os


"""
Proportion of schools with access to: 
(a) electricity; 
(b) the Internet for pedagogical purposes; 
(c) computers for pedagogical purposes; 
(d) adapted infrastructure and materials for students with disabilities; 
(e) basic drinking water; 
(f) single-sex basic sanitation facilities; and 
(g) basic handwashing facilities (as per the WASH indicator definitions)

	geo_id VARCHAR NOT NULL, 
	year VARCHAR NOT NULL, 
	deped_id VARCHAR,
	water VARCHAR,
	internet VARCHAR,
	electricity VARCHAR,
	computers VARCHAR,
	disability_infrastructure VARCHAR,
	sanitation_facilities VARCHAR,
	ss_sanitation_facilities VARCHAR,
	handwashing_facilities VARCHAR
"""

ids = pd.read_csv("../../files_for_db/geo/khm_geo.csv")
id_dict = dict(zip(ids["deped_id"], ids["geo_id"]))
print(ids.head())


# Fetch and read the datasets
DATA_PATH = str(os.path.abspath(os.path.join(__file__ ,"../../.."))) + "/data/KHM/"
khm_schools = gpd.read_file(DATA_PATH + "Basic information of school (2014)/basic_information_of_school_2014.shp")
khm_schools = khm_schools.to_crs("epsg:4326")

khm_schools = khm_schools[["SCHOOL_COD", "SWATER"]].rename(columns = {"SCHOOL_COD": "deped_id", "SWATER": "water"})


khm_schools["water"] = khm_schools["water"].astype(int)



# # extract year from date
khm_schools["year"] = 2014


# # merge to get geo_ids


# add columns with no values
khm_schools["internet"] = -99
khm_schools["electricity"] = -99
khm_schools["computers"] = -99
khm_schools["handwashing_facilities"] = -99
khm_schools["sanitation_facilities"] = -99
khm_schools["ss_sanitation_facilities"] = -99
khm_schools["disability_infrastructure"] = -99

khm_schools = pd.merge(khm_schools, ids[["geo_id", "deped_id"]], on = "deped_id")

khm_schools = khm_schools[["geo_id", "year", "deped_id", "water", "internet", "electricity", "computers", "disability_infrastructure", "sanitation_facilities", "ss_sanitation_facilities", "handwashing_facilities"]]

print(khm_schools['internet'].value_counts())

print(khm_schools.head())

# # export
khm_schools.to_csv("../../files_for_db/resources/khm_resources.csv", index = False)