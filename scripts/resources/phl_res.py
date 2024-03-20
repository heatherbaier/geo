import pandas as pd

"""
Proportion of schools with access to: 
(a) electricity; 
(b) the Internet for pedagogical purposes; 
(c) computers for pedagogical purposes; 
(d) adapted infrastructure and materials for students with disabilities; 
(e) basic drinking water; 
(f) single-sex basic sanitation facilities; and 
(g) basic handwashing facilities (as per the WASH indicator definitions)
"""

ids = pd.read_csv("../../archive/phl_geo.csv")

data = pd.read_csv("../../data/PHL/this_one.csv")
data = data.rename(columns = {"school_id": "deped_id"})

data = pd.merge(data, ids, on = "deped_id")

data = data[["geo_id", "school_year", "deped_id", "original_water_boolean", "original_internet_boolean", "original_electricity_boolean"]]

data = data.rename(columns = {"original_water_boolean": "water", "original_internet_boolean": "internet", "original_electricity_boolean": "electricity", "school_year": "year"})

data["computers"] = -99
data["disability_infrastructure"] = -99
data["sanitation_facilities"] = -99
data["ss_sanitation_facilities"] = -99
data["handwashing_facilities"] = -99


print(data.head())

print(data.columns)

data = data.to_csv("../../files_for_db/resources/phl_resources.csv", index = False)