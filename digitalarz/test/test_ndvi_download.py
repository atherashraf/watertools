# # -*- coding: utf-8 -*-
# """
# Created on Wed Nov 16 07:21:48 2022
#
# @author: timhe
# """
import os.path
import pandas as pd
import shutil

import requests
import watertools
from osgeo import gdal
from pyhdf.HDF import HDF, HC
from pyhdf.SD import SD, SDC
from pyhdf.V import *
from pyhdf.VS import *

from watertools.digitalarz.hdf_reader import HDFReader


def download_file(file_name: str):
    username, password = watertools.Functions.Random.Get_Username_PWD.GET('NASA')
    # print("username: %s" % username)
    # print("password: %s" % password)
    #
    x = requests.get(
        'https://e4ftl01.cr.usgs.gov/MOLT/MOD13Q1.061/2021.11.17/MOD13Q1.A2021321.h23v05.061.2021338161613.hdf',
        allow_redirects=False)
    try:
        y = requests.get(x.headers['location'], auth=(username, password))
    except:
        from requests.packages.urllib3.exceptions import InsecureRequestWarning

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        y = requests.get(x.headers['location'], auth=(username, password), verify=False)
    # with open(file_name, 'wb') as out_file:
    #     shutil.copyfileobj(y.raw, out_file)

    z = open(file_name, 'wb')
    z.write(y.content)
    z.close()


def read_hdf_file(file_name: str):
    hdf_reader = HDFReader(file_name)
    datasets = hdf_reader.get_dataset_names()
    # print(datasets)
    # hdf_reader.to_geotiff_all()

    # tiff_path = f"{file_name[:-4]}/250m 16 days NDVI.tif"
    # ds = gdal.Open(tiff_path)
    ds = hdf_reader.to_gdal_dataset('250m 16 days NDVI')
    print(ds)



if __name__ == "__main__":
    file_path = "temp/test_data/ndvi/mod13"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    fn = f'{file_path}/MOD13Q1.A2021321.h23v05.061.2021338161613.hdf'
    # if os.path.exists(fn):
    #     os.remove(file_name)
    if not os.path.exists(fn):
        download_file(fn)

    read_hdf_file(fn)
