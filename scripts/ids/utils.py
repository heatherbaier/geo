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
    to_open = [i for i in os.listdir(tmp_dir) if i.endswith(".zip") and i.startswith('geo')]

    # Extract the files from the second zipfolder
    with zipfile.ZipFile(os.path.join(tmp_dir, to_open[0]), 'r') as zip_ref:
        zip_ref.extractall(tmp_dir)
    
    # Clean up directory
    to_delete = [i for i in os.listdir(tmp_dir) if i.endswith(".zip") or i.startswith('geo')]
    for i in to_delete:
      os.remove(os.path.join(tmp_dir, i))
    
    print("Done downloading boundary data.")



def getGBpath(iso, adm, base_dir):

    files = os.listdir(os.path.join(base_dir, iso))
    shp = [_ for _ in files if ".shp" in _][0]
    fname = os.path.join(base_dir, iso, shp)

    return fname