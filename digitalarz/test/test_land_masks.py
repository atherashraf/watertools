# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 19:27:24 2022

@author: timhe
"""
import datetime
import os
import traceback

import numpy as np
import watertools.General.raster_conversions as RC
import watertools.General.data_conversions as DC
from osgeo import gdal

try:
    folder_input_ETLook_Static = r"/Users/atherashraf/PycharmProjects/DigitalArz/IPI/media/Output_Data/ETLook/ETLook_input_composite/Static"
    folders_input_RAW = r"/Users/atherashraf/PycharmProjects/DigitalArz/IPI/media/Input_Data"
    NDVI_file = r"/Users/atherashraf/PycharmProjects/DigitalArz/IPI/media/Output_Data/ETLook/ETLook_input_composite/20220101/NDVI_20220101.tif"  # one tiff file from

    Date = datetime.datetime(2022, 1, 1)
    LandCover = "GlobCover"

    # Get example files
    dest_ex = gdal.Open(NDVI_file)
    geo_ex = dest_ex.GetGeoTransform()
    proj_ex = dest_ex.GetProjection()
    size_x_ex = dest_ex.RasterXSize
    size_y_ex = dest_ex.RasterYSize

    LM_file = os.path.join(folder_input_ETLook_Static, "LandMask_%s.tif" % Date.year)
    Bulk_file = os.path.join(folder_input_ETLook_Static, "Bulk_Stomatal_resistance_%s.tif" % Date.year)
    MaxObs_file = os.path.join(folder_input_ETLook_Static, "Maximum_Obstacle_Height_%s.tif" % Date.year)
    LUEmax_file = os.path.join(folder_input_ETLook_Static, "LUEmax_%s.tif" % Date.year)
    print(LM_file)
    print(Bulk_file)
    print(MaxObs_file)
    print(LUEmax_file)
    if not (os.path.exists(LM_file) and os.path.exists(Bulk_file) and os.path.exists(MaxObs_file) and os.path.exists(
            LUEmax_file)):

        if LandCover == "GlobCover":
            folder_RAW_file_LC = os.path.join(folders_input_RAW, "GlobCover", "Landuse")
            filename_LC = "LC_GLOBCOVER_V2.3.tif"
        if LandCover == "WAPOR":
            folder_RAW_file_LC = os.path.join(folders_input_RAW, "L1_LCC_A")
            filename_LC = "L1_LCC_A_WAPOR_YEAR_%s.01.01.tif" % (Date.year)

        if os.path.exists(os.path.join(folder_RAW_file_LC, filename_LC)):
            destLC = RC.reproject_dataset_example(os.path.join(folder_RAW_file_LC, filename_LC), NDVI_file, method=1)
            LC = destLC.GetRasterBand(1).ReadAsArray()
            LC[np.isnan(LC)] = -9999

            # import list with numbers to convert globcover into other maps
            import pywapor.general.landcover_converter as LCC

            if LandCover == "GlobCover":
                # Get conversion between globcover and landmask
                LU_LM_Classes = LCC.Globcover_LM()
                LU_Bulk_Classes = LCC.Globcover_Bulk()
                LU_MaxObs_Classes = LCC.Globcover_MaxObs()
                LU_LUEmax_Classes = LCC.Globcover_LUEmax()

            if LandCover == "WAPOR":
                # Get conversion between globcover and landmask
                LU_LM_Classes = LCC.WAPOR_LM()
                LU_Bulk_Classes = LCC.WAPOR_Bulk()
                LU_MaxObs_Classes = LCC.WAPOR_MaxObs()
                LU_LUEmax_Classes = LCC.WAPOR_LUEmax()

            # Create Array for LandMask
            LM = np.ones([size_y_ex, size_x_ex]) * np.nan
            Bulk = np.ones([size_y_ex, size_x_ex]) * np.nan
            MaxObs = np.ones([size_y_ex, size_x_ex]) * np.nan
            LUEmax = np.ones([size_y_ex, size_x_ex]) * np.nan

            # Create LandMask
            for LU_LM_Class in LU_LM_Classes.keys():
                Value_LM = LU_LM_Classes[LU_LM_Class]
                Value_Bulk = LU_Bulk_Classes[LU_LM_Class]
                Value_MaxObs = LU_MaxObs_Classes[LU_LM_Class]
                Value_LUEmax = LU_LUEmax_Classes[LU_LM_Class]
                LM[LC == LU_LM_Class] = Value_LM
                Bulk[LC == LU_LM_Class] = Value_Bulk
                MaxObs[LC == LU_LM_Class] = Value_MaxObs
                LUEmax[LC == LU_LM_Class] = Value_LUEmax

            # Save as tiff files
            DC.Save_as_tiff(LM_file, LM, geo_ex, proj_ex)
            DC.Save_as_tiff(Bulk_file, Bulk, geo_ex, proj_ex)
            DC.Save_as_tiff(MaxObs_file, MaxObs, geo_ex, proj_ex)
            DC.Save_as_tiff(LUEmax_file, LUEmax, geo_ex, proj_ex)

        else:
            print("LandCover is not available")

    print("done")
except:
    traceback.print_exc()
