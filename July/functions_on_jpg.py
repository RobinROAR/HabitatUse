#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import Image
from glob import glob
import os
import numpy as np
import re

def tif2jpg(inputfile,outputfile, cnt):
    src = inputfile
    if cnt == 0:
        os.system('gdal_translate -of JPEG {0} {1}'.format(inputfile,outputfile))
    else:
        os.system('gdal_translate -of JPEG {0} {1}'.format(inputfile, outputfile))


def image2tiles(w,h,folder):
    #遍历图片
    imgs = glob(folder+'*.jpg')
    for img in imgs:
        name = img.lstrip(folder).rstrip('.jpg')

        if os.path.exists(folder+name):
            os.system('rm -rf {0}'.format(folder+name))
        else:
            os.mkdir(folder+name)

        #process
        #get basic image infomation
        im = Image.open(img)
        ds = np.array(im)
        width,height = ds.shape[1],ds.shape[0]

        #get the number of tiles
        numx = width/w
        numy = height/h
        cnt = 0
        #split
        y = 0
        for i in range(numy):
            x=0
            y+=h
            for j in range(numx):
                x += w
                cnt+=1
                im.crop((x-w,y-h,x,y)).save(folder+name+'/'+name+'{0}.jpg'.format(str(cnt)))
        print 'finish spliting: sum {}'.format(str(numx*numy))

def merge_images():

    UNIT_SIZE = 256  # 单个图像的大小为229*229
    TARGET_WIDTH = 2 * UNIT_SIZE  # 拼接完后的横向长度为6*229

    path = "data/jpg"
    images = []
    #遍历图像文件夹，联结目录与图像名，存储到两个list中
    for root,dirs,files in os.walk(path):
        if len(dirs) == 0:
            temp =[os.path.join(root,i) for i in files ]
            images.append(temp)
        else:
            continue
    #配对图像
    cnt = 0
    for i in images[0]:
        for j in images[1]:
            if i.split('.')[0].split('_')[2] == j.split('.')[0].split('_')[2]   :
                print i,j
                #拼接
                #新建图像
                target = Image.new('RGB',(TARGET_WIDTH, UNIT_SIZE))
                left = 0
                right = UNIT_SIZE
                #将image复制到target的指定位置中
                target.paste(Image.open(i), (left, 0, right, UNIT_SIZE))
                target.paste(Image.open(j), (left+UNIT_SIZE, 0, right+UNIT_SIZE, UNIT_SIZE))
                cnt+=1
                #os.mkdir('./data/jpg/{0}'.format(i.split('/')[2].split('R')[0]))
                target.save('./data/jpg/{1}.jpg'.format(i.split('/')[2].split('R')[0],cnt),quality_value = 100)
            else:
                continue

    # for root,     left += UNIT_SIZE  # left是左上角的横坐标，依次递增                                                                    dirs, files in os.walk(path):
    #     for f     right += UNIT_SIZE  # right是右下的横坐标，依次递增                                                                   in files:
    #         im    quality_value = 100  # quality来指定生成图片的质量，范围是0～100                                                         ages.append(f)
    # for i in r    target.save(path + '/result/' + os.path.splitext(images[i * 6 + j])[0] + '.jpg', quality=quality_value)   ange(len(images) / 6):  # 6个图像为一组
    #     imagefile = []
    #     j = 0
    #     for j in range(6):
    #         imagefile.append(Image.open(path + '/' + images[i * 6 + j]))
    #     target = Image.new('RGB', (TARGET_WIDTH, UNIT_SIZE))
    #     left = 0
    #     right = UNIT_SIZE
    #     for image in imagefile:
    #         target.paste(image, (left, 0, right, UNIT_SIZE))  # 将image复制到target的指定位置中
    #         left += UNIT_SIZE  # left是左上角的横坐标，依次递增
    #         right += UNIT_SIZE  # right是右下的横坐标，依次递增
    #         quality_value = 100  # quality来指定生成图片的质量，范围是0～100
    #         target.save(path + '/result/' + os.path.splitext(images[i * 6 + j])[0] + '.jpg', quality=quality_value)
    #     imagefile = []



if __name__ == '__main__':

    #image2tiles(256,256,'data/jpg/')

    merge_images()

    #tif2jpg('data/modis/new.tif', 'data/temp/05252007H_.jpg',0)
    #tif2jpg('data/modis/newH.tif','data/temp/05252007R_.jpg',1)

    # im1 = Image.open('data/temp/05252007H.jpg')
    # im2 = Image.open('data/temp/05252007R.jpg')
    # im = Image.blend(im1,im2,0.2)
    # im.show()