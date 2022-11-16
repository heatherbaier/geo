import pandas as pd
import os


IDS_DIR = "../../files_for_db/coordinates/"

for i, (file) in enumerate(os.listdir(IDS_DIR)):
    file = os.path.join(IDS_DIR, file)
    if i == 0:
        df = pd.read_csv(file)
    else:
        df = df.append(pd.read_csv(file))

df["index"] = [_ for _ in range(0, len(df))]
df = df[["index", "geo_id", "longitude", "latitude"]]

df = df.drop_duplicates(subset = ["geo_id"])

print(df.shape)

df.to_csv("../../files_for_db/db/coordinates.csv", index = False)