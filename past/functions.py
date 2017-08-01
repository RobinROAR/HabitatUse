import csv
import os,sys,time,gdal
from gdalconst import *

	
def readFromTxt(filename):
	f=open(filename,'rb')
	for line in f:
		x1, y1, x2,y2 = line.split(",")    
		print (x2,y2)
		
def readRaster(tif):
	gdal.AllRegister()
	ds = gdal.Open(tif,GA_ReadOnly)
	if  ds is None:
		print 'Could not find the RasterData'
		sys.exit(1)
	print 'Raster Info: '+'bandscount '+str(ds.RasterCount)
		
		#get raster's info
	transform = ds.GetGeoTransform()
	bands = ds.RasterCount   
	band = ds.GetRasterBand(1)
	xOrigin = transform[0]
	yOrigin = transform[3]
	pixelWidth = transform[1]
	pixelHeight = transform[5]
	
	print xOrigin  
	print yOrigin
	print pixelWidth
	print pixelHeight


def writeCsv(filename,contents):
	
	writer = csv.writer(file(filename,'wb'))
	writer.writerow()
	for line in contents:
		writer.writerow(line)
		print line
		
