import csv
import os,sys,time,gdal
from gdalconst import *


def readFromCsv(filename):
	
	global all_pos
	csvFile=file(filename,'rb')
	reader=csv.reader(csvFile)
	for line in reader:
		if reader.line_num == 1:  
			continue  		
		pos = [line[0],line[1]]                             
		all_pos.append(pos)
			
	print('all_pos:'+str(len(all_pos)))
	
def readFromTxt(filename):
	f=open(filename,'rb')
	for line in f:
		x1, y1, x2,y2 = line.split(",")    
		print (x2,y2)
		
def readRaster(enviname):
	gdal.AllRegister()
	global envi
	for tif in enviname:
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

		nXsize = 1  #What's this     
		nYsize = 1
		
		index=0
		for pos in all_pos:
			x = int((float(pos[0])-xOrigin)/pixelWidth)
			y = int((float(pos[1])-yOrigin)/pixelHeight)
			data = band.ReadAsArray(x,y,1,1)
			
			value = data[0,0]     #What's 0,0 meaning
			envi[index].append(value)
			#print len(envi[index])
			index+=1
		print index

def writeCsv():
	global envi,enviname
	
	writer = csv.writer(file('M2.csv','wb'))
	writer.writerow(enviname)
	for line in envi:
		writer.writerow(line)
		print line
		
#=======start main
#~ startTime = time.time()

rows=175
cols =250
#coordinate group
all_pos=[]   
#envi 2-dimen matrix
envi=[]
for i in range(rows*cols):
	envi.append([])

inputfilename='pos.csv'
enviname=['water.tif','Artificial.tif','croplands.tif','bare.tif','forest.tif']

readFromCsv(inputfilename)
readRaster(enviname)
writeCsv()

#========end main
endTime= time.time()
print 'It took '+str(round((endTime-startTime),3)) +' s '


