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

    #  for each file in the geo folder...
    for file in os.listdir("./personnel"):

        # extract the iso from the filename
        iso = file.split("_")[0]

        '''
        get the number of non-null values in each column AND the total number of rows in the df and save that to the country dict as {iso:{column:count}}
        for the year column - instead of getting the number of non-null values, get a list of unique years
        for the geo_id column - instead of getting the number of non-null values, get a count of unique values
        '''
        df = pd.read_csv(f"./personnel/{file}")
        country_dict[iso] = {}
        for col in df.columns:
            if col == "year":
                country_dict[iso][col] = df[col].unique().tolist()
            elif col in ["geo_id", "deped_id"]:
                country_dict[iso][col] = df[col].nunique()
            else:
                country_dict[iso][col] = df[col].count()
        # country_dict[iso] = df.count().to_dict()
        country_dict[iso]["total_rows"] = df.shape[0]
    # then transofrm that to a df
    country_df = pd.DataFrame(country_dict).T

    # add a column to the beginning for total number of rows in each country


    # convert coluns to integers
    country_df = country_df.fillna(0)
    country_df = country_df.reset_index().rename(columns = {"index": "iso"}).sort_values(by = "iso", ascending = False)
    print(country_df.head())
    print(country_df.shape) 


    country_df.to_csv("personnel_review4.csv", index = False)
