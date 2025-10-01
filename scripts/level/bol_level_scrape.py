
from bs4 import BeautifulSoup
import pandas as pd
import requests

import warnings
warnings.filterwarnings("ignore")


def scrape_school_long(school_id):
    url = f"https://seie.minedu.gob.bo/reportes/mapas_unidades_educativas/ficha/ver/{school_id}"
    r = requests.get(url, verify=False)

    soup = BeautifulSoup(r.text, "html.parser")

    # --- 1. Extract "Nivel" ---
    # Find the <dt> with text "Nivel(es):" and get the next <dd>
    nivel_dt = soup.find("dt", string=lambda t: t and "Nivel(es)" in t)
    nivel = None
    if nivel_dt:
        nivel_dd = nivel_dt.find_next_sibling("dd")
        if nivel_dd:
            nivel = nivel_dd.get_text(strip=True)

    # print(nivel)

    # Parse all tables
    tables = pd.read_html(r.text)
    vars_ = ["matricula", "promovidos", "reprobados", "abandonos"]
    records = []

    for var, df in zip(vars_, tables):
        # Keep only relevant rows
        df = df[df["Sexo"].isin(["Total", "Mujer", "Hombre"])]
        year_cols = [c for c in df.columns if c.isdigit()]

        for year in year_cols:
            total_val = df.loc[df["Sexo"] == "Total", year].values[0]
            female_val = df.loc[df["Sexo"] == "Mujer", year].values[0] if "Mujer" in df["Sexo"].values else 0
            male_val = df.loc[df["Sexo"] == "Hombre", year].values[0] if "Hombre" in df["Sexo"].values else 0

            records.append({
                "school_id": school_id,
                "year": int(year),
                "variable": var,
                "total": total_val,
                "female": female_val,
                "male": male_val
            })

    df = pd.DataFrame(records)

    pivoted = df.pivot_table(
        index=["school_id", "year"], 
        columns="variable", 
        values=["total", "female", "male"]
    )

    # Flatten MultiIndex: becomes total_abandonos, female_promovidos, etc.
    pivoted.columns = [f"{var}_{col}" for col, var in pivoted.columns]
    pivoted = pivoted.reset_index()

    pivoted["nivel"] = nivel

    return pivoted


gdf = pd.read_csv("../../data/BOL/bol_schools_from_wms.csv")
gdf = gdf.dropna(subset = ["cod_ue"])
print(gdf.shape)

# Example usage
school_ids = gdf["cod_ue"].unique()  # replace with your real IDs
for c, scid in enumerate(school_ids):
    print(c, len(school_ids), end = "\r")
    scrape_school_long(scid).to_csv(f"../../data/BOL/scrape/{scid}.csv")

# print(df.head())
