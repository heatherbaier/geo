import pandas as pd
import argparse
import os

if __name__ == "__main__":
    
    # parser = argparse.ArgumentParser()
    # parser.add_argument('iso', type = str)
    # args = parser.parse_args() 

    # df = pd.read_csv(f"./{args.iso}_geo.csv")
    # print(df.head())
    # print(df.shape)

    # 

    # Run the script
    # print number of non-null values in each column

    country_dict = {}
    #  for each file in the geo folder, extract the iso from the filename, get the number of non-null values in each column AND the total number of rows in the df and save that to the country dict as {iso:{column:count}}, then transofrm that to a df

    for file in os.listdir("./geo"):
        iso = file.split("_")[0]
        df = pd.read_csv(f"./geo/{file}")
        country_dict[iso] = df.count().to_dict()
        country_dict[iso]["total_rows"] = df.shape[0]
    country_df = pd.DataFrame(country_dict).T

    # add a column to the beginning for total number of rows in each country


    # convert coluns to integers
    country_df = country_df.fillna(0)
    country_df = country_df.astype(int).reset_index().rename(columns = {"index": "iso"}).sort_values(by = "iso", ascending = False)
    print(country_df.head())
    print(country_df.shape) 


    country_df.to_csv("geo_review.csv", index = False)
