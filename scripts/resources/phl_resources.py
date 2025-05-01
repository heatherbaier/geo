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
"""

ids = pd.read_csv("../../files_for_db/geo/phl_geo.csv")

data = pd.read_csv("../../data/PHL/this_one.csv")
data = data.rename(columns = {"school_id": "deped_id"})

data = pd.merge(data, ids, on = "deped_id")

data = data[["geo_id", "school_year", "deped_id", "original_water_boolean", "original_internet_boolean", "original_electricity_boolean"]]

data = data.rename(columns = {"original_water_boolean": "water", "original_internet_boolean": "internet", "original_electricity_boolean": "electricity", "school_year": "year"})

data["computers"] = np.nan
data["disability_infrastructure"] = np.nan
data["sanitation_facilities"] = np.nan
data["ss_sanitation_facilities"] = np.nan
data["handwashing_facilities"] = np.nan


print(data.head())

print(data.columns)


# replace all instances of True in the dataframe with 1 and all instances of False with 0 as integers
data = data.replace({True: 1, False: 0})

# convert all columns to integers
data["year"] = data["year"].fillna(np.nan).astype('Int64')
data["water"] = data["water"].fillna(np.nan).astype('Int64')
data["electricity"] = data["electricity"].fillna(np.nan).astype('Int64')
data["internet"] = data["internet"].fillna(np.nan).astype('Int64')
data["computers"] = data["computers"].fillna(np.nan).astype('Int64')
data["disability_infrastructure"] = data["disability_infrastructure"].fillna(np.nan).astype('Int64')
data["sanitation_facilities"] = data["sanitation_facilities"].fillna(np.nan).astype('Int64')
data["ss_sanitation_facilities"] = data["ss_sanitation_facilities"].fillna(np.nan).astype('Int64')
data["handwashing_facilities"] = data["handwashing_facilities"].fillna(np.nan).astype('Int64')


data = data.to_csv("../../files_for_db/resources/phl_resources.csv", index = False)