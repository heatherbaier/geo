import pandas as pd

#get data from github and choose necessary columns
usa_table = pd.read_csv("../../data/USA/ccd_sch_029_2122_w_1a_071722.csv", dtype={"LZIP":str})
usa_table = usa_table[["SCH_NAME", "SCHID", "LSTREET1", "LCITY", "LSTATE","LZIP", "STATENAME"]]

#create necessary columns
usa_table["address"] = usa_table["LSTREET1"] + ", " + usa_table["LCITY"] + ", " + usa_table["LSTATE"] + " " + usa_table["LZIP"]

usa_table.reset_index(inplace=True)
usa_table['geo_id'] = usa_table['index'].apply(lambda x: 'USA-{0:0>6}'.format(x))

usa_table["adm0"] = "USA"
usa_table["adm3"] = None

#choose final columns and rename
usa_table = usa_table[["geo_id", "SCHID", "SCH_NAME", "address", "adm0", "STATENAME", "LCITY", "adm3"]]
usa_table.columns = ["geo_id", "country_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3"]

#export as csv
usa_table.to_csv("../../files_for_db/ids/usa_ids.csv", index=False)