# -*-coding:utf-8 -*-
import sys
import os
import shutil



class Partition:
    def __init__(self, folderpath):
        self.path = folderpath

    def repackage(self):
        '''
        提取相同时间戳，放入同一文件
        :return:
        '''
        #遍历文件夹信息
        for dirpath, dirnames, filenames in os.walk(self.path):
            self.dirpath = dirpath
            self.files = filenames
            self.root =dirpath
            break
        #取公共时间戳
        timestamp = []
        for _ in self.files:
            temp = _.split('.')
            if temp[-1] == 'hdf':
                timestamp.append(temp[0]+temp[1])
        #创建文件夹
        timestamp = list(set(timestamp))
        for _ in timestamp:
            if os.path.exists(os.path.join(self.dirpath,_)):
                print "Folder exists: "+ os.path.join(self.dirpath,_)
            else:
                os.mkdir(os.path.join(self.dirpath,_))

        #移动文件
        for _ in self.files:
            suffix = os.path.splitext(os.path.join(self.dirpath,_))
            if suffix[1] == '.xml' or suffix[1] == '.hdf':
                temp = _.split('.')
                if temp[0]+temp[1] == timestamp[0]:
                    shutil.move(os.path.join(self.dirpath,_),os.path.join(self.dirpath,timestamp[0],_))
                if temp[0] + temp[1] == timestamp[1]:
                    shutil.move(os.path.join(self.dirpath, _), os.path.join(self.dirpath, timestamp[1],_))


if __name__ == "__main__":
    pa = Partition('./data')
    pa.repackage()
