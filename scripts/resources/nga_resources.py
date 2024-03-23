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
data = data[["geo_id", "year", "water", "sanitation_facilities"]]

# add columns with no values
data["internet"] = -99
data["computers"] = -99
data["disability_infrastructure"] = -99
data["ss_sanitation_facilities"] = -99
data["handwashing_facilities"] = -99

# export
data.to_csv("../../files_for_db/resources/nga_resources.csv", index = False)