import pandas as pd
import numpy as np
from utils import *

#import necessary data from github
nga_table = pd.read_csv("../../data/NGA/educational-facilities-in-nigeria.csv")
nga_ids_table = pd.read_csv("../../files_for_db/ids/nga_ids.csv")

#create new year column with data from original source
nga_table["year"] = nga_table["date_of_survey"].str[:4]

#merge with id table to get geo ids
nga_table["deped_id"] = nga_table["facility_id"]
nga_table = pd.merge(nga_table, nga_ids_table, how="inner")

#final formatting
nga_table_resources = nga_table[["geo_id", "year", "improved_water_supply", "phcn_electricity"]]

nga_table_resources["internet"] = None
nga_table_resources["library"] = None
nga_table_resources["cafeteria"] = None

nga_table_resources = nga_table_resources[["geo_id", "year", "improved_water_supply", "internet", "phcn_electricity", "library", "cafeteria"]] 
nga_table_resources.columns = ["geo_id", "year", "water", "internet", "electricity", "library", "cafeteria"]

#export final table as csv
nga_table_resources.to_csv("../../files_for_db/resources/nga_res.csv", index=False)