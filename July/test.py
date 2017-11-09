#!/usr/bin/env python
# -*- coding:utf-8 -*-July23 2017
#Robin
from PIL import Image
from glob import glob
import os
import numpy as np
import shutil


def listjpg(path):
    #遍历文件夹
    folders = None
    for root,dir,file in os.walk(path):
        if len(dir)!=0:
            folders = [os.path.join(root,d) for d in dir]
        else:
            continue
    #分离图片
    cnt = 1
    for _ in folders:
        imgs = glob(_+'/*.jpg')
        for i in imgs:
            shutil.copyfile(i, 'data/train/'+str(cnt)+'.jpg')
            cnt += 1






listjpg('data/train/')


