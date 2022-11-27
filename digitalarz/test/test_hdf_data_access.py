import os
import traceback

import numpy as np
from osgeo import gdal
"""
test code for HDF in DataAccess.py
line no 397 to 456 under collect data function
"""
from watertools.digitalarz.hdf_reader import HDFReader

file_name = '/Users/atherashraf/PycharmProjects/DigitalArz/IPI/media/Input_Data/LST/MOD11/8_Daily/MOD11A2.A2022001.h23v05.061.2022010050239.hdf'
day_night = 'day'
Horizontal = 23
Vertical = 5
TilesHorizontal = [23.0, 24.0]
TilesVertical = [5.0, 6.0]

sizeX = int((TilesHorizontal[1] - TilesHorizontal[0] + 1) * 1200)
sizeY = int((TilesVertical[1] - TilesVertical[0] + 1) * 1200)

countX = Horizontal - TilesHorizontal[0] + 1
countY = (TilesVertical[1] - TilesVertical[0] + 1) - (Vertical - TilesVertical[0])
TimeStep = 8
angle_info = 0
DataTot = np.zeros((sizeY, sizeX))
DataTot_Time = np.zeros((sizeY, sizeX))
DataTot_ObsAng = np.zeros((sizeY, sizeX))
Distance = 4 * 231.65635826395834
try:

    # Open .hdf only band with NDVI and collect all tiles to one array
    # dataset = gdal.Open(file_name)
    # sdsdict = dataset.GetMetadata('SUBDATASETS')
    # if day_night == "day":
    #     sdslist = [sdsdict[k] for k in sdsdict.keys() if
    #                (('SUBDATASET_1_NAME') in k or ('SUBDATASET_3_NAME') in k or ('SUBDATASET_4_NAME') in k)]
    # else:
    #     sdslist = [sdsdict[k] for k in sdsdict.keys() if
    #                (('SUBDATASET_5_NAME') in k or ('SUBDATASET_7_NAME') in k or ('SUBDATASET_8_NAME') in k)]
    hdf_reader = HDFReader(file_name)
    dataset_names = hdf_reader.get_dataset_names()
    # sdslist = []
    if day_night == "day":
        sdslist = [dataset_names[k] for k in [0, 2, 3]]
    else:
        sdslist = [dataset_names[k] for k in [4, 6, 7]]
    sds = []
    sds_time = []
    sds_obsang = []

    for n in sdslist:
        sds.append(hdf_reader.to_gdal_dataset(n))
        if day_night == "day":
            full_layer = [i for i in sdslist if 'LST_Day_1km' in i]
        else:
            full_layer = [i for i in sdslist if 'LST_Night_1km' in i]
        idx = sdslist.index(full_layer[0])
        if Horizontal == TilesHorizontal[0] and Vertical == TilesVertical[0]:
            geo_t = sds[idx].GetGeoTransform()

            # get the projection value
            proj = sds[idx].GetProjection()

        data = sds[idx].ReadAsArray()
        countYdata = (TilesVertical[1] - TilesVertical[0] + 2) - countY
        DataTot[int((countYdata - 1) * 1200):int(countYdata * 1200),
        int((countX - 1) * 1200):int(countX * 1200)] = data * 0.02
    del data

    if TimeStep == 1:
        if day_night == "day":
            full_layer_time = [i for i in sdslist if 'Day_view_time' in i]
        else:
            full_layer_time = [i for i in sdslist if 'Night_view_time' in i]
        idx_time = sdslist.index(full_layer_time[0])
        sds_time.append(gdal.Open(sdslist[idx_time]))
        data_time = sds_time[0].ReadAsArray()
        DataTot_Time[int((countYdata - 1) * 1200):int(countYdata * 1200),
        int((countX - 1) * 1200):int(countX * 1200)] = data_time * 0.1
        del data_time

    if angle_info == 1:
        if day_night == "day":
            full_layer_obsang = [i for i in sdslist if 'Day_view_angl' in i]
        else:
            full_layer_obsang = [i for i in sdslist if 'Night_view_angl' in i]
        idx_obsang = sdslist.index(full_layer_obsang[0])
        sds_obsang.append(gdal.Open(sdslist[idx_obsang]))
        data_obsang = sds_obsang[0].ReadAsArray()
        DataTot_ObsAng[int((countYdata - 1) * 1200):int(countYdata * 1200),
        int((countX - 1) * 1200):int(countX * 1200)] = data_obsang
        del data_obsang
    print("done")
    # if the tile not exists or cannot be opened, create a nan array with the right projection
except Exception as e:
    if Horizontal == TilesHorizontal[0] and Vertical == TilesVertical[0]:
        x1 = (TilesHorizontal[0] - 19) * 1200 * Distance
        x4 = (TilesVertical[0] - 9) * 1200 * -1 * Distance
        geo = [x1, Distance, 0.0, x4, 0.0, -Distance]
        geo_t = tuple(geo)
    traceback.print_exc()

