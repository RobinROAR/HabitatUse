#!/usr/bin/env python
# -*- coding:utf-8 -*-

#Test file

import pandas as pd
import numpy as np
from osgeo import gdal,ogr,osr,gdalnumeric
import os

def shp2raster():

    # Define pixel_size and NoData value of new raster
    NoData_value = 0
    # Filename of input OGR file
    vector_fn = 'data/shp/testBuffer.shp'
    # Filename of the raster Tiff that will be created
    raster_fn = 'data/temp/circle.tif'
    # Open the data source and read in the extent
    source_ds = ogr.Open(vector_fn)
    source_layer = source_ds.GetLayer()
    #x_min, x_max, y_min, y_max = source_layer.GetExtent()
    x_min, x_max, y_min, y_max = 99.2, 101.011, 36.255, 37.625

    # 读取geotransform
    ds = gdal.Open('data/landsat/final.tif')
    geotransform = ds.GetGeoTransform()
    # Create the destination data source
    x_res = ds.RasterXSize
    y_res = ds.RasterYSize
    ds = None
    # 设定投影
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    target_ds = gdal.GetDriverByName('GTiff').Create(raster_fn, x_res, y_res, 1, gdal.GDT_Byte)

    target_ds.SetGeoTransform(geotransform)
    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(NoData_value)
    # Rasterize
    gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[255])
    print 'shp2raster finished'

if __name__ == '__main__':
    shp2raster()