import pandas as pd
import numpy as np
from utils import *

#import necessary data from github
phl_raw = pd.read_csv("../../data/PHL/this_one.csv")
phl_ids = pd.read_csv("../../files_for_db/ids/phl_ids.csv")

#select and rename necessary columns
phl_resources = phl_raw[["school_year", "school_id", "original_water_boolean", "original_internet_boolean", "original_electricity_boolean"]]
phl_resources.rename(columns = {"school_year":"year", "school_id":"deped_id", "original_water_boolean":"water", "original_internet_boolean":"internet", "original_electricity_boolean":"electricity"}, inplace=True)

#merge to get geo_ids
phl_resources = pd.merge(phl_resources, phl_ids, how="inner")

#add final columns and reorganize
phl_resources["library"] = None
phl_resources["cafeteria"] = None
phl_resources = phl_resources[["geo_id", "year", "water", "internet", "electricity", "library", "cafeteria"]]

#export as csv
phl_resources.to_csv("../../files_for_db/resources/phl_res.csv", index = False)