import pandas as pd
import numpy as np

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


# import ids
ids = pd.read_csv("../../files_for_db/geo/pry_geo.csv")

# use only geo_id and deped_id from id file
ids = ids[["geo_id", "deped_id"]]


# # import raw resources data
data = pd.read_csv("/Users/heatherbaier/Documents/geo_git/data/PRY/instituciones_2012.csv")
data = data[["codigo_establecimiento", "tiene_internet"]]
data = data.rename(columns = {"codigo_establecimiento": "deped_id"})

data["internet"] = data["tiene_internet"].map({"NO": 0, "SI": 1, "": np.nan})

data["internet"] = data["internet"].astype("Int64")

# print(data.head())
# print(data["tiene_internet"].value_counts())
# print(data["internet"].value_counts())

data["year"] = 2012
data["year"] = data["year"].astype("Int64")


# add columns with no values
data["water"] = np.nan
data["electricity"] = np.nan
data["computers"] = np.nan
data["handwashing_facilities"] = np.nan
data["sanitation_facilities"] = np.nan
data["ss_sanitation_facilities"] = np.nan
data["disability_infrastructure"] = np.nan

data = pd.merge(data, ids[["geo_id", "deped_id"]], on = "deped_id", how = "right")

data = data[["geo_id", "year", "deped_id", "water", "internet", "electricity", "computers", "disability_infrastructure", "sanitation_facilities", "ss_sanitation_facilities", "handwashing_facilities"]]

print(data.head())

data.to_csv("../../files_for_db/resources/pry_resources.csv", index = False)