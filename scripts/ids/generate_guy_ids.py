import pandas as pd
from utils import *

#import data
guy_table = pd.read_excel("../../data/GUY/National list of Schools  (1).xlsx")

#add region name as adm1
#GT stands for Georgetown, the capital of Guyana, and it is in region 4
guy_table["adm1"] = guy_table["REGION"].str.replace("01", "Barima-Waini").replace("02", "Pomeroon-Supernaam").replace("03", "Essequibo Islands-West Demerara").replace(["04", "GT"], "Demerara-Mahaica").replace("05", "Mahaica-Berbice").replace("06", "East Berbice-Corentyne").replace("07", "Cuyuni-Mazaruni").replace("08", "Potaro-Siparuni").replace("09", "Upper Takutu-Upper Essequibo").replace("10", "Upper Demerara-Berbice")

#format strings in columns
guy_table["SCHOOL NAME"] = guy_table["SCHOOL NAME"].str.title()
guy_table["ADDRESS"] = guy_table["ADDRESS"].str.title()

#add geo_ids
guy_table.reset_index(inplace=True)
guy_table['geo_id'] = guy_table['index'].apply(lambda x: 'GUY-{0:0>6}'.format(x))

#create table of only useful columns from original data
guy_ids_table = guy_table[["geo_id", "SCHOOL NAME", "ADDRESS", "adm1"]]

#add, rename, and sort columns
guy_ids_table["deped_id"] = None
guy_ids_table["adm0"] = "GUY"
guy_ids_table["adm2"] = None
guy_ids_table["adm3"] = None
guy_ids_table.columns = ["geo_id", "school_name", "address", "adm1", "deped_id", "adm0", "adm2", "adm3"]
guy_ids_table = guy_ids_table[["geo_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3"]]

#export as csv
guy_ids_table.to_csv("../../files_for_db/ids/guy_ids.csv", index = False)
