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

    df.sort_values(['dattime'], ascending = 0)


    return df

if __name__ == '__main__':

    d = readData()
    print d