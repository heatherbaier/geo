import geopandas as gpd
import pandas as pd

from utils import *

per_ef = pd.read_csv("../../data/PER/Relación de instituciones y programas educativos.csv")
print(per_ef.columns)
per_ef = per_ef.drop_duplicates(subset = ["cod_mod"])
per_ef['cen_edu'] = per_ef['cen_edu'].str.replace('\d+', '')
per_ef = per_ef[["cod_mod", "cen_edu", "nlong_ie", "nlat_ie"]]
per_ef = per_ef.reset_index()
per_ef['geo_id'] = per_ef['index'].apply(lambda x: 'PER-{0:0>6}'.format(x))
per_ef = per_ef.drop(["index"], axis = 1)
per_ef = per_ef[["geo_id", "cod_mod", "cen_edu", "nlong_ie", "nlat_ie"]].rename(columns = {"cod_mod": "deped_id", "cen_edu": "school_name", "nlong_ie": "longitude", "nlat_ie": "latitude"})
per_ef["address"] = None
per_ef["adm0"] = "PER"
print(per_ef.head())

# Geocode to ADM levels
cols = ["geo_id", "deped_id", "school_name", "longitude", "latitude", "address", "adm0"]
for adm in range(1, 4):

    try:

        cols += ["adm" + str(adm)]
        downloadGB("PER", str(adm), "../../gb")
        shp = gpd.read_file(getGBpath("PER", str(adm), "../../gb"))
        per_ef = gpd.GeoDataFrame(per_ef, geometry = gpd.points_from_xy(per_ef.longitude, per_ef.latitude))
        per_ef = gpd.tools.sjoin(per_ef, shp, how = "left").rename(columns = {"shapeName": "adm" + str(adm)})[cols]
        print(per_ef)

    except Exception as e:

        per_ef["adm" + str(adm)] = None
        print(e)

per_ef = per_ef[cols].drop(["longitude", "latitude"], axis = 1)

print(per_ef.head())

per_ef.to_csv("../../files_for_db/ids/per_ids.csv", index = False)
