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
    #temp = df[(df.animal.isin(['BH07_67582','BH07_67690','BH07_67695','BH07_67698','BH07_ 74898']))&(df.datetime <= pd.to_datetime('2007-09-25 03:00:00')) & (df.datetime >= pd.to_datetime('2007-03-25 03:00:00'))]
    #temp = df[(df.datetime <= pd.to_datetime('2008-09-25 03:00:00')) & (df.datetime >= pd.to_datetime('2008-02-25 03:00:00')) ]
    #论文图表
    temp = df[(df.animal.isin(['BH07_67582','BH07_67690','BH07_67695','BH07_67698','BH07_ 74898']))&(df.datetime <= pd.to_datetime('2008-12-25 03:00:00')) & (df.datetime >= pd.to_datetime('2008-01-25 03:00:00'))]
    print df.groupby('animal').count()


    #temp = df[df.animal.isin(['BH07_67582', 'BH07_67690', 'BH07_67695', 'BH07_67698', 'BH07_74898'])]
    #遍历结果
    for index,row in temp.loc[:, ['longitude', 'latitude']].iterrows():
        #if (row.longitude >= 99.2)&(row.longitude<=101.011)&(row.latitude<=37.625)&(row.latitude>=36.255):
        if (row.longitude >= 96.6) & (row.longitude <= 101.1) & (row.latitude <= 37.6) & (row.latitude >= 34.5):
            result.append([row.longitude,row.latitude])
    #return result
    print len(result)


if __name__ == '__main__':

    d = readData()
    #fs.create_shp_points(d)