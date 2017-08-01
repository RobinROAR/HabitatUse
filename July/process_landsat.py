#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Test file

import pandas as pd
from glob import glob
import numpy as np
from osgeo import gdal,ogr,osr,gdalnumeric
import os


def merge_landsat(src,bands):
    #通过dict储存不同波段对应的文件
    result = {'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[]}
    for root, dirs, files in os.walk(src):
        #print root,dirs,files
        if len(dirs) == 0:
            for _ in files:
                if '.TIF' in _:
                    # 通过dict储存每个波段对应的文件
                    for i in range(1,8):
                        if 'B'+str(i) in _:
                            result[str(i)].append(os.path.join(root,_))
                    else:
                        continue
                else:
                    continue
        else:
            continue

    #merge tif
    for i in range(1,bands+1):
        t1,t2 = result[str(i)][0],result[str(i)][1]
        #-n: set notata-value
        os.system('gdal_merge.py -of GTiff -n 0 -o {0} {1}'.format('data/landsat/'+str(i)+'.tif',t1+' '+t2))
    return 'merge finished'

def bands_conbine(path,bands):
    #combine selected bands into one tif
    os.system('gdal_merge.py -seperate 1.tif 2.tif 3.tif -o out.tif ')

def clip(inshp,inraster,outraster):
    os.system('gdalwarp -cutline %s %s %s -crop_to_cutline'% (inshp,inraster,outraster))

def reproject(infile,outfile):
    os.system('gdalwarp %s %s -r near -t_srs EPSG:4326' % (infile,outfile))
    return 'warp ok. generate'+outfile

if __name__ == '__main__':
    #tif2jpg('data/temp/final.tif','data/temp/final.jpg')


    #合成每个

   #merge_landsat('data/landsat',7)

    #矩形裁剪
    clip('data/shp/rec.shp','data/landsat/stack.tif', 'data/landsat/repro.tif')
    #重投影
    reproject('data/landsat/repro.tif','data/landsat/final.tif')

