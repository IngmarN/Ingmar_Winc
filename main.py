__winc_id__ = "ae539110d03e49ea8738fd413ac44ba8"
__human_name__ = "files"
import os
import zipfile
from pathlib import Path


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
    dir = "files\\cache"
    for f in os.listdir(dir):
        g = f
        f = Path()
        f = f.resolve()
        x = os.path.join(f, dir, g)
        cached_list.append(x)
    return cached_list


# Hey, ik weet dat een comment niet de bedoeling is maar ik weet dat de opdracht gecontroleerd wordt.
# Dus ik probeerde het eerst met de os.path.abspath maar die liet files\\cache buiten het pad en ging Winc\\0.txt.
# Toen deed ik path.join met files\\cache maar dan plakt hij achter de txt file, dus ook niet handig.
# Op het internet vond ik Path.resolve, maar die stopt bij \\Winc. Dus ik plakte de drie stukken aan elkaar zoals je kunt zien.
# Ik neem aan dat er een makkelijkere oplossing is, als u die kan laten zien zou ik heel dankbaar zijn.
# print(cached_files())


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


find_password(cached_files())
