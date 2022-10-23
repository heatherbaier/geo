import pandas as pd

df = pd.read_csv("../../data/PRY/pry_coords.csv")
df = df[["anio", "codigo_est", "xcoord", "ycoord"]]

print(df.head())

