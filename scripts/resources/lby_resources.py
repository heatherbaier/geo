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

# import geo_ids and only select columns for merging
ids = pd.read_csv("../../files_for_db/geo/lby_geo.csv")
ids = ids[["geo_id", "deped_id"]]

# import raw resources data
data = pd.read_csv("../../data/LBY/reach_lby_nationalschoolsassessment_complete_db_reliable__not_reliable_18oct2012.csv", low_memory=False)
data = data.rename(columns = {"QI_eSchoolID": "deped_id"})

# print(data.head())
# print(data.shape)
# print(pd.merge(data, ids, on = "deped_id").shape)

# data = pd.merge(data, ids, on = "deped_id")

# agag

# check if each resource is present and ensure that it wasn't damaged
data["electricity"] = np.where((data["Q4_6Electricity"] > 0) & (data["Q4_4_2Damage1"].isnull()), 1, 0)
data["water"] = np.where((data["Q3_2DrinkingWater"] > 0) & (data["Q4_4_2Damage2"].isnull()), 1, 0)
data["sanitation_facilities"] = np.where((data["Q3_3Toilets6"] > 0) & (data["Q4_4_2Damage3"].isnull()), 1, 0)
data["handwashing_facilities"] = np.where((data["Q3_6WashingHands"] > 0) & (data["Q4_4_2Damage3"].isnull()), 1, 0)

# rename school id column to merge with geo_id
data.rename(columns={'QI_eSchoolID': 'deped_id'}, inplace=True)
data = pd.merge(data, ids, on = "deped_id")

# for resources not present in the data, set as None
data["year"] = 2012
data["internet"] = None
data["computers"] = None
data["disability_infrastructure"] = None
data["ss_sanitation_facilities"] = None

# select necessary columns
data = data[["geo_id",
             "year",
             "deped_id",
			 "water",
             "electricity",
             "internet",
             "computers",
             "disability_infrastructure",
             "sanitation_facilities",
			 "ss_sanitation_facilities",
             "handwashing_facilities"]]

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




# save as csv
data.to_csv("../../files_for_db/resources/lby_resources.csv", index = False)