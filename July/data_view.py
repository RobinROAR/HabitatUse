#!/usr/bin/env python
# -*- coding:utf-8 -*-July23 2017
#Robin
from PIL import Image
from glob import glob
import os
import numpy as np



#
# kde = KernelDensity(bandwidth=0.04, metric='haversine',
#                     kernel='gaussian', algorithm='ball_tree')
# kde.fit(points)

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import geoplotlib

def readData():
    # 读取数据至dataframe
    df = pd.read_csv('./data/birdDataLG.csv')
    df.columns = [u'animal', u'lon', u'lat', u'datetime']
    # 转换datetime为时间格式
    df['datetime'] = pd.to_datetime(df.datetime)
    # 先将日期转换为时间个事，在比较
    temp = df[(df.animal.isin(['BH07_67582', 'BH07_67690', 'BH07_67695', 'BH07_67698', 'BH07_74898'])) & (df.datetime <= pd.to_datetime('2007-09-25 03:00:00')) & (df.datetime >= pd.to_datetime('2007-05-25 03:00:00'))]
    #temp = df[(df.datetime <= pd.to_datetime('2007-5-25 03:00:00')) & (df.datetime >= pd.to_datetime('2007-03-25 03:00:00')) ]
    # temp = df[df.animal.isin(['BH07_67582', 'BH07_67690', 'BH07_67695', 'BH07_67698', 'BH07_74898'])]


    print temp.count()
    # 遍历结果
    return temp



def writeCSV(a):
    a.to_csv("test.csv")






temp = readData()

def add_corner(temp):

    temp.loc[temp.index.max() + 1] = {'animal':'ed', 'lon': 99.49,'lat':37.5,'datetime' : ''}
    print temp.count(),'++++++++++++++++'+str(temp.shape[0]+1)
    temp.loc[temp.index.max() + 1]  = {'animal':'ed', 'lon': 99.49,'lat':36.3,'datetime' : ''}
    print temp.count(),'++++++++++++++++'+str(temp.shape[0]+1)
    temp.loc[temp.index.max() + 1]  = {'animal':'ed1', 'lon': 100.97,'lat':37.5,'datetime' : ''}
    print temp.count(),'++++++++++++++++'+str(temp.shape[0]+1)
    temp.loc[temp.index.max() + 1]  = {'animal':'ed1', 'lon': 100.97,'lat':36.3,'datetime' : ''}
    print temp.count(),'++++++++++++++++'+str(temp.shape[0]+1)
    writeCSV(temp)


#add_corner(temp)
data = geoplotlib.utils.DataAccessObject(temp)
geoplotlib.dot(data)
#geoplotlib.kde(data,0.1)
geoplotlib.show()



