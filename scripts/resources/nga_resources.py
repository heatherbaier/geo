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


	# geo_id VARCHAR NOT NULL, 
	# year VARCHAR NOT NULL, 
	# deped_id VARCHAR,
	# water VARCHAR,
	# internet VARCHAR,
	# electricity VARCHAR,
	# computers VARCHAR,
	# disability_infrastructure VARCHAR,
	# sanitation_facilities VARCHAR,
	# ss_sanitation_facilities VARCHAR,
	# handwashing_facilities VARCHAR


# import ids
ids = pd.read_csv("../../files_for_db/geo/nig_geo.csv")

# use only geo_id and deped_id from id file
ids = ids[["geo_id", "deped_id"]]

# import raw resources data
data = pd.read_csv("../../data/NGA/educational-facilities-in-nigeria.csv", low_memory=False)

# extract year from date
data["year"] = data["date_of_survey"].str[:4]

# get only needed columns from data and rename
data = data[["improved_water_supply", "improved_sanitation", "facility_id", "year"]]
data.columns = ["water", "sanitation_facilities", "deped_id", "year"]

# merge to get geo_ids
data = pd.merge(data, ids, on = "deped_id")

# reorder columns
# i also got rid of deped_id in this step, so it can be re-added in this line as needed
data = data[["geo_id", "year", "deped_id", "water", "sanitation_facilities"]]

# add columns with no values
data["electricity"] = np.nan
data["internet"] = np.nan
data["computers"] = np.nan
data["disability_infrastructure"] = np.nan
data["ss_sanitation_facilities"] = np.nan
data["handwashing_facilities"] = np.nan


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

print(data.dtypes)


# replace all instances of True in the dataframe with 1 and all instances of False with 0 as integers
data = data.replace({True: 1, False: 0})

# convert all columns to integers
data["water"] = data["water"].fillna(np.nan).astype('Int64')
data["electricity"] = data["electricity"].fillna(np.nan).astype('Int64')
data["internet"] = data["internet"].fillna(np.nan).astype('Int64')
data["computers"] = data["computers"].fillna(np.nan).astype('Int64')
data["disability_infrastructure"] = data["disability_infrastructure"].fillna(np.nan).astype('Int64')
data["sanitation_facilities"] = data["sanitation_facilities"].fillna(np.nan).astype('Int64')
data["ss_sanitation_facilities"] = data["ss_sanitation_facilities"].fillna(np.nan).astype('Int64')
data["handwashing_facilities"] = data["handwashing_facilities"].fillna(np.nan).astype('Int64')



# export
data.to_csv("../../files_for_db/resources/nga_resources.csv", index = False)