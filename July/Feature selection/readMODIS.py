#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Robin @ Aug 28


import math
import csv
import os,sys,time,gdal
import random
import scipy.stats as st
from gdalconst import *
import csv
import gdal
import numpy as np


# read CSV
def readFromCsv(filename):
    all_pos = []
    csvFile = file(filename, 'rb')
    reader = csv.reader(csvFile)
    for line in reader:
        if reader.line_num == 1:
            continue
        pos = [line[2], line[3]]
        if (float(line[2])<100.97 and float(line[2])> 99.49 and float(line[3])> 36.3 and float(line[3])<37.5):
            all_pos.append(pos)
        else:
            continue

    #print('all_pos:' + str(len(all_pos)))
    return all_pos


def random_pos():
    rad = np.random.uniform(low = [99.94,36.3],high = (100.97,37.5),size=[388,2])
    return rad


def readData(f1, tifname):
    print '************: ' + tifname
    global RcountNum
    global countNum

    #获取鸟类坐标
    birds = readFromCsv(f1)
    #获取随即坐标
    rad = list(random_pos())
    #birds+=rad

    # get raster's info
    ds = gdal.Open(tifname, GA_ReadOnly)
    if ds is None:
        print 'Could not find the RasterData'
        sys.exit(1)
    transform = ds.GetGeoTransform()
    bands = ds.RasterCount
    band = ds.GetRasterBand(1)
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]

    # read and count
    result = []
    for pos in birds:
        x = int((float(pos[0]) - xOrigin) / pixelWidth)
        y = int((float(pos[1]) - yOrigin) / pixelHeight)
        data = band.ReadAsArray(x, y, 1, 1)  # data is Array
        value = data[0, 0]  # 0,0 is top left
        result.append(value)
    result = np.array(result)
    return result



path1 = './data/0625-479.csv'
tif_path = [
    '/home/robin/GitProject/HabitatUse/July/Feature selection/1/MOD09A1A2007169_sur_refl_b01_MOD_Grid_500m_Surface_Reflectance.tif',
    '/home/robin/GitProject/HabitatUse/July/Feature selection/1/MOD09A1A2007169_sur_refl_b02_MOD_Grid_500m_Surface_Reflectance.tif',
    '/home/robin/GitProject/HabitatUse/July/Feature selection/1/MOD09A1A2007169_sur_refl_b03_MOD_Grid_500m_Surface_Reflectance.tif',
    '/home/robin/GitProject/HabitatUse/July/Feature selection/1/MOD09A1A2007169_sur_refl_b04_MOD_Grid_500m_Surface_Reflectance.tif',
    '/home/robin/GitProject/HabitatUse/July/Feature selection/1/MOD09A1A2007169_sur_refl_b05_MOD_Grid_500m_Surface_Reflectance.tif',
    '/home/robin/GitProject/HabitatUse/July/Feature selection/1/MOD09A1A2007169_sur_refl_b06_MOD_Grid_500m_Surface_Reflectance.tif',
    '/home/robin/GitProject/HabitatUse/July/Feature selection/1/MOD09A1A2007169_sur_refl_b07_MOD_Grid_500m_Surface_Reflectance.tif',
    ]
# tif_path = ['/home/robin/GitProject/HabitatUse/July/Feature selection/data/1/MOD13Q1A2007161_250m_16_days_blue_reflectance_MODIS_Grid_16DAY_250m_500m_VI.tif',
#             '/home/robin/GitProject/HabitatUse/July/Feature selection/data/1/MOD13Q1A2007161_250m_16_days_EVI_MODIS_Grid_16DAY_250m_500m_VI.tif',
#             '/home/robin/GitProject/HabitatUse/July/Feature selection/data/1/MOD13Q1A2007161_250m_16_days_MIR_reflectance_MODIS_Grid_16DAY_250m_500m_VI.tif',
#             '/home/robin/GitProject/HabitatUse/July/Feature selection/data/1/MOD13Q1A2007161_250m_16_days_NDVI_MODIS_Grid_16DAY_250m_500m_VI.tif',
#             '/home/robin/GitProject/HabitatUse/July/Feature selection/data/1/MOD13Q1A2007161_250m_16_days_NIR_reflectance_MODIS_Grid_16DAY_250m_500m_VI.tif',
#             '/home/robin/GitProject/HabitatUse/July/Feature selection/data/1/MOD13Q1A2007161_250m_16_days_red_reflectance_MODIS_Grid_16DAY_250m_500m_VI.tif',
#             ]
path2 = '/home/robin/GitProject/HabitatUse/July/Feature selection/data/1/1/0610-1-KDE.TIF'

features= ['blue','EVI','MIR','NDVI','NIR','red']

features= ['1','2','3','4','5','6','7']

r = readData(path1,tif_path[1])

result = np.zeros((388,7),dtype = np.float64)
for i in range(7):
    r = readData(path1,tif_path[i])
    result[:,i] = r
    r = None


#原始获得标签的方法
t = readData(path1,path2)
target = np.array(t,dtype=np.float64)


# target = np.append(np.zeros(388),np.ones(388))


#_______________________________________________________________________________________
#特征选择
from sklearn.cross_validation import cross_val_score, ShuffleSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression




X = result
Y = target

names = features


rf = RandomForestRegressor(n_estimators=10, max_depth=5,max_features=3)
rf.fit(X, Y)
print "Features sorted by their score:"
print sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names),
             reverse=True)

lasso = Lasso(alpha=.3)
lasso.fit(X, Y)
def pretty_print_linear(coefs, names = None, sort = False):
    if names == None:
        names = ["X%s" % x for x in range(len(coefs))]
    lst = zip(coefs, names)
    if sort:
        lst = sorted(lst, key = lambda x:-np.abs(x[0]))
    return " + ".join("%s * %s" % (round(coef, 3), name) for coef, name in lst)

print "Lasso model: ", pretty_print_linear(lasso.coef_, names, sort = True)

lr = LinearRegression()
lr.fit(X, Y)
print "Linear model:", pretty_print_linear(lr.coef_,names, sort = True)

ridge = Ridge(alpha=0.1)
ridge.fit(X, Y)
print "Ridge model:", pretty_print_linear(ridge.coef_,names, sort = True)


