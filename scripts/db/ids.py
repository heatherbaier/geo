import pandas as pd
import os


IDS_DIR = "../../files_for_db/ids/"

for i, (file) in enumerate(os.listdir(IDS_DIR)):
    file = os.path.join(IDS_DIR, file)
    if i == 0:
        df = pd.read_csv(file)
    else:
        df = df.append(pd.read_csv(file))


for col in df.columns:
    df[col] = df[col].str.encode('ascii', 'ignore').str.decode('ascii')

print(df.shape)

df.to_csv("../../files_for_db/db/ids.csv", index = False)