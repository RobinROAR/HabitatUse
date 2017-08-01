#!/usr/bin/env python
# -*- coding:utf-8 -*-

#Test file

import pandas as pd
import functions_on_shp as fs
import numpy
from osgeo import ogr,osr
import os

def readData():
    result = []
    #读取数据至dataframe
    df = pd.read_csv('./data/birdDataLG.csv')
    #转换datetime为时间格式
    df['datetime'] = pd.to_datetime(df.datetime)
    #先将日期转换为时间个事，在比较
    temp = df[(df.animal.isin(['BH07_67582','BH07_67690','BH07_67695','BH07_67698','BH07_74898']))&(df.datetime <= pd.to_datetime('2007-09-25 03:00:00')) & (df.datetime >= pd.to_datetime('2007-03-25 03:00:00'))]
    #temp = df[(df.datetime <= pd.to_datetime('2007-09-25 03:00:00')) & (df.datetime >= pd.to_datetime('2007-03-25 03:00:00')) ]
    #temp = df[df.animal.isin(['BH07_67582', 'BH07_67690', 'BH07_67695', 'BH07_67698', 'BH07_74898'])]
    #遍历结果
    for index,row in temp.loc[:, ['longitude', 'latitude']].iterrows():
        if (row.longitude >= 99.2)&(row.longitude<=101.011)&(row.latitude<=37.625)&(row.latitude>=36.255):
            result.append([row.longitude,row.latitude])
    return result


if __name__ == '__main__':

    d = readData()
    fs.create_shp_points(d)