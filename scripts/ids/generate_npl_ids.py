import pandas as pd
import numpy as np
from utils import *

#import data and combine into one file
npl_table_raw1 = pd.read_csv("../../data/NPL/School Performance for the year 2062 BS.csv")
npl_table_raw2 = pd.read_csv("../../data/NPL/School Performance for the year 2063 BS.csv")

npl_table_raw1 = npl_table_raw1[["District", "Zone", "School Code", "Name of School"]]
npl_table_raw2 = npl_table_raw2[["District", "Zone", "School Code", "Name of School"]]

npl_table_raw = pd.concat([npl_table_raw1, npl_table_raw2])

npl_table = npl_table_raw.drop_duplicates().reset_index()

#create new index column
npl_table.drop("index", axis=1, inplace=True)
npl_table.reset_index(inplace=True)

#rename, delete, and add columns
npl_table.rename(columns = {"Zone":"adm1", "District":"adm2", "School Code":"deped_id", "Name of School":"school_name"}, inplace=True)
npl_table['geo_id'] = npl_table['index'].apply(lambda x: 'NPL-{0:0>6}'.format(x))
npl_table["address"] = None
npl_table["adm0"] = "NGL"
npl_table["adm3"] = None
npl_table = npl_table[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3"]]

#export as csv
npl_table.to_csv("../../files_for_db/ids/npl_ids.csv", index = False)
