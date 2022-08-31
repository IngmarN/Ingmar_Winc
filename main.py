__winc_id__ = "ae539110d03e49ea8738fd413ac44ba8"
__human_name__ = "files"

import os
import zipfile


def clean_cache():
    dir = 'files/cache'
    if os.path.isdir(dir):
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
    else:
        os.mkdir(dir)


def cache_zip(zip_path, cache_path):
    clean_cache()
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(cache_path)


def cached_files():
    cached_list = []
    path = os.getcwd()
    path2 = os.path.join(path, "files", "cache")
    for f in os.listdir(path2):
        x = os.path.join(path2, f)
        cached_list.append(x)
    return cached_list


def find_password(cached_list):
    for f in cached_list:
        path = f
        file = open(f, "r")
        file = file.read()
        file_split = file.split()
        count = 0
        for x in file_split:
            count += 1
            if x == "password" or x == "pass" or x == "pass:" or x == "password:":
                return file_split[count]
