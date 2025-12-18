import requests
import argparse
import zipfile
import shutil
import json
import os


def makeGBdir(iso, base_dir):
  
    # If the folder already exists, delete it
    if os.path.isdir(os.path.join(base_dir, iso)):
        shutil.rmtree(os.path.join(base_dir, iso))
    else:
        "Couldn't delete old folder"
    
    # Create new folder
    try:
        os.mkdir(os.path.join(base_dir, iso))
    except:
        os.mkdir(base_dir)
        os.mkdir(os.path.join(base_dir, iso))

    # ...and return the path
    return os.path.join(base_dir, iso)


def downloadGB(iso, adm, base_dir):

    # Create the request URL
    url = "https://www.geoboundaries.org/api/current/gbOpen/" + iso + "/ADM" + adm
    print("Making request to: ", url)

    # Make the request to the URL
    r = requests.get(url)
    dlPath = r.json()['staticDownloadLink']
    print("Downloading data from: ", dlPath)
    
    # Get the download URL
    r = requests.get(dlPath, allow_redirects=True)

    # Make directory for downloaded zipfolder
    tmp_dir = makeGBdir(iso, base_dir)
    print("Downloading data into: ", tmp_dir)
    
    # Open the request and download the zipfolder
    open(os.path.join(tmp_dir, "temp.zip"), 'wb').write(r.content)

    # Open the downloaded zipfolder
    with zipfile.ZipFile(os.path.join(tmp_dir, "temp.zip"), 'r') as zip_ref:
        zip_ref.extractall(tmp_dir)

    # Grab the name of the second zipfolder
    # to_open = [i for i in os.listdir(tmp_dir) if i.endswith(".zip") and i.startswith('geo')]

    # # Extract the files from the second zipfolder
    # with zipfile.ZipFile(os.path.join(tmp_dir, to_open[0]), 'r') as zip_ref:
    #     zip_ref.extractall(tmp_dir)
    
    # # Clean up directory
    # to_delete = [i for i in os.listdir(tmp_dir) if i.endswith(".zip") or i.startswith('geo')]
    # for i in to_delete:
    #   os.remove(os.path.join(tmp_dir, i))
    
    print("Done downloading boundary data.")



def getGBpath(iso, adm, base_dir):

    files = os.listdir(os.path.join(base_dir, iso))
    shp = [_ for _ in files if ".shp" in _][0]
    fname = os.path.join(base_dir, iso, shp)

    return fname


import os
import shutil
import geopandas as gpd

def process_geo_file(df, iso, gb_path="../../gb", csv_out=None, shp_out=None):
    """
    Process and geocode a country's school data to ADM0-ADM3 boundaries,
    filter to points inside ADM0, and save to CSV and Shapefile.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe with at least 'longitude' and 'latitude' columns.
    iso : str
        ISO3 country code (e.g., "BHR").
    gb_path : str
        Path to location where GADM (or other) admin boundary files are stored/downloaded.
    csv_out : str
        Path to output CSV file (optional).
    shp_out : str
        Path to output shapefile folder (optional).
    """

    csv_out = f"../../files_for_db/geo/{iso.lower()}_geo.csv"
    shp_out = f"../../files_for_db/shps/{iso.lower()}"

    df = df.copy()
    df["adm0"] = iso

    print(f"[INFO] Processing {iso}, starting shape: {df.shape}")

    # --- ADM0 filter ---
    downloadGB(iso, "0", gb_path)
    adm0 = gpd.read_file(getGBpath(iso, "ADM0", gb_path))
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs=adm0.crs)
    gdf = gpd.sjoin(gdf, adm0[["geometry"]], how="inner", predicate="within").drop(columns="index_right")
    print(f"[INFO] After ADM0 filter: {gdf.shape}")

    # Save original coords (so they persist after joins)
    longs, lats = gdf["longitude"].values, gdf["latitude"].values

    # --- ADM1-ADM3 geocoding ---
    cols = ["oedc_id", "deped_id", "school_name", "adm0", "address"]
    for adm in range(1, 4):
        try:
            cols += [f"adm{adm}"]
            downloadGB(iso, str(adm), gb_path)
            shp = gpd.read_file(getGBpath(iso, f"ADM{adm}", gb_path))
            gdf = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(gdf.longitude, gdf.latitude))
            gdf = gpd.tools.sjoin(gdf, shp, how="left").rename(columns={"shapeName": f"adm{adm}"})[cols]
            gdf["longitude"], gdf["latitude"] = longs, lats
            print(f"[INFO] ADM{adm} join successful, shape: {gdf.shape}")
        except Exception as e:
            gdf[f"adm{adm}"] = None
            print(f"[WARN] ADM{adm} join failed: {e}")

    # Reorder columns
    gdf = gdf[["oedc_id", "deped_id", "school_name", "address", "adm0", "adm1", "adm2", "adm3", "longitude", "latitude"]]

    # --- Save CSV ---
    if csv_out:
        os.makedirs(os.path.dirname(csv_out), exist_ok=True)
        gdf.to_csv(csv_out, index=False)
        print(f"[INFO] CSV saved to {csv_out}")

    # --- Save Shapefile ---
    if shp_out:
        os.makedirs(shp_out, exist_ok=True)
        gdf_out = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(gdf.longitude, gdf.latitude), crs="EPSG:4326")
        shp_file = os.path.join(shp_out, f"{iso.lower()}.shp")
        gdf_out.to_file(shp_file, index=False)
        shutil.make_archive(shp_out, 'zip', shp_out)
        print(f"[INFO] Shapefile saved to {shp_file} and zipped.")

    return gdf
