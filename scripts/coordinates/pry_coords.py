import pandas as pd
from utils import *

#import necessary data from github
pry_raw = pd.read_csv("../../data/PRY/pry_coords.csv")
pry_ids = pd.read_csv("../../files_for_db/ids/pry_ids.csv")

#select and rename columns
pry_coord = pry_raw[["codigo_est", "ycoord", "xcoord"]]
pry_coord.rename(columns={"codigo_est":"deped_id", "ycoord":"latitude", "xcoord":"longitude"}, inplace=True)

#merge for geo_ids
pry_coord = pd.merge(pry_coord, pry_ids, how="inner")
pry_coord = pry_coord[["geo_id", "longitude", "latitude"]]

#export as csv
pry_coord.to_csv("../../files_for_db/coordinates/pry_coordinates.csv", index = False)
