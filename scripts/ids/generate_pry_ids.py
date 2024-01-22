import pandas as pd
from utils import *

#import data
pry_ids = pd.read_csv("../../data/PRY/pry_coords.csv")

#select and rename columns
pry_ids = pry_ids[["codigo_est", "nombre_dep", "nombre_dis", "direccion"]]
pry_ids.rename(columns = {"codigo_est":"deped_id", "nombre_dep":"adm1", "nombre_dis":"adm2", "direccion":"school_name"}, inplace=True)

#create geo_ids
pry_ids.reset_index(inplace=True)
pry_ids['geo_id'] = pry_ids['index'].apply(lambda x: 'PRY-{0:0>6}'.format(x))

#create and reorder columns
pry_ids["address"] = None
pry_ids["adm0"] = "PRY"
pry_ids["adm3"] = None

pry_ids = pry_ids[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3"]]

#export as csv
pry_ids.to_csv("../../files_for_db/ids/pry_ids.csv", index = False)