import urllib.request
import os
import json
import zipfile

def fetch_all():
    path = os.getcwd()
    abs_path = os.path.join(path[:path.index("SeminarniPraceM") + len("SeminarniPraceM")], "src/tmp")
    abs_path_sources = os.path.join(path[:path.index("SeminarniPraceM") + len("SeminarniPraceM")], "src/website/sources.json")

    #get JSON sources
    f = open(abs_path_sources)
    URLS = json.load(f)

    #delete all current files
    for filename in os.listdir(abs_path):
        file_path = os.path.join(abs_path, filename)
        if os.path.isfile(file_path) and filename != ".gitkeep":
            os.remove(file_path)

    #fetch all the ZIPs
    for (key, val) in URLS.items():
        urllib.request.urlretrieve(val, os.path.join(abs_path, key + ".zip"))
    
    #unzip all ZIPs and delete them
    for filename in os.listdir(abs_path):
        file_path = os.path.join(abs_path, filename)
        if os.path.isfile(file_path) and filename != ".gitkeep":
            with zipfile.ZipFile(file_path, "r") as zip_file:
                zip_file.extractall(abs_path)
            
            os.remove(file_path)

if __name__ == "__main__":
    fetch_all()