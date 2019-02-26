#Robin  
#Cnic Beijing   
#2014.06.06

import MySQLdb
import math
import csv
import os,sys,time,gdal
import random
import scipy.stats as st

from gdalconst import *

#preferences  参数选择  QHL
#~ C1=[[11,21],[30,101],[110,131],[140,151],[160,200],[210,221]]        #landuse
#~ C2=[[-1,-0.5],[-0.5,0],[0,0.25],[0.25,0.4],[0.4,1]]      				#ndvi07
#~ C3 =[[2800,3200],[3200,3300],[3300,3400],[3400,3600],[3600,4000]]		#dem
#~ C4 = [[0,500],[500,2000],[2000,4000],[4000,99999999]]         	#waterDistance
#~ C5 = [[0,200],[200,500],[500,2000],[2000,99999]]             #road distace
#~ Category =[C1,C2,C3,C4,C5]
#~ tif = ['tif/07QHH/landuse.tif','tif/07QHH/NDVI/ndvi07.tif','tif/07QHH/dem/qhhdem.tif','tif/07QHH/waterDistance/waterDistance.tif','tif/07QHH/road/road.tif']
#~ pos = ['point/QHH/QHLPU.csv','point/QHH/QHLPA.csv']

 # 参数选择ＬＲＷ
C1=[[11,21],[30,101],[110,131],[140,151],[160,200],[210,219],[220,300]]    #landuse
C2=[[-1,-0.5],[-0.5,0],[0,0.25],[0.25,1]]      				#ndvi
C3 =[[2800,3500],[3500,3800],[3800,4200],[4200,5600]]		#dem
C4 = [[0,500],[500,2000],[2000,4000],[4000,99999999]]         	#waterDistance
Category =[C1,C2,C3,C4]
tif = ['tif/LRW/landuselrw/landuselrw.tif','tif/LRW/NDVI/ndvilrw1.tif','tif/LRW/dem/lrdem.tif','tif/LRW/WD/wdlrw1.tif']
pos = ['point/LRW/LRWPU.csv','point/LRW/LRWPA.csv']


#DataNum use to  store  Birds' records num 
dataNum = []

#read CSV
def readFromCsv(filename):
	
	all_pos=[]
	csvFile=file(filename,'rb')
	reader=csv.reader(csvFile)
	for line in reader:
		if reader.line_num == 1:  
			continue  		
		pos = [line[1],line[2]]                             
		all_pos.append(pos)
			
	print('all_pos:'+str(len(all_pos)))
	return all_pos


def readData(f1,f2,tifname,Category):			
	
	print '************: '+tifname
	global RcountNum
	global countNum
	
	
	randomList = readFromCsv(f2)
	listT = readFromCsv(f1)
	
	#get raster's info
	ds = gdal.Open(tifname,GA_ReadOnly)
	if  ds is None:
		print 'Could not find the RasterData'
		sys.exit(1)
	transform = ds.GetGeoTransform()
	bands = ds.RasterCount   
	band = ds.GetRasterBand(1)
	xOrigin = transform[0]
	yOrigin = transform[3]
	pixelWidth = transform[1]
	pixelHeight = transform[5]

	#read and count
	for pos in listT:
		x = int((float(pos[0])-xOrigin)/pixelWidth)
		y = int((float(pos[1])-yOrigin)/pixelHeight)
		data = band.ReadAsArray(x,y,1,1)            #data is Array
		value = data[0,0]                                      #0,0 is top left
		i = 0
		for cate in Category:
			if ((value >=cate[0])&(value<cate[1])):
				countNum[i]+=1
			i+=1
			
	#read random and count
	for pos in randomList:
		x = int((float(pos[0])-xOrigin)/pixelWidth)
		y = int((float(pos[1])-yOrigin)/pixelHeight)
		data = band.ReadAsArray(x,y,1,1)            #data is Array
		value = data[0,0]                                      #0,0 is top left
		i = 0
		for cate in Category:
			if ((value >=cate[0])&(value<cate[1])):
				RcountNum[i]+=1
			i+=1

#main loop begin
for j in range(len(tif)):
	#countNum use to store every categories' num
	countNum = [0]*len(Category[j])
	RcountNum=[0]*len(Category[j])	
	
	readData(pos[0],pos[1],tif[j],Category[j])			

	print '---------------------------------------------------'
	#store  result  and print

	sumU=0
	numU=[]
	freU=[]
	print 'used num && frequency: '
	for element in countNum:
		sumU+=element
	for element in countNum:
		numU.append(element)
		freU.append(float(element)/sumU)
		print '%-40s %-9.3f' % (element,float(element)/sumU)

	print '----------------------------------------------------'

	numA=[]
	freA=[]
	sumA=0
	print 'availiable  num && frequency: '
	for element in RcountNum:
		sumA+=element
	for element in RcountNum:
		numA.append(element)
		freA.append(float(element)/sumA)
		print  '%-40d %9.3f' % (element,float(element)/sumA)
	

	#calculate the result

	Z=st.norm.ppf(1-0.05/(2*len(Category[j])))

	wiList=[]                                       #value of   ui/ai
	seWiList=[]                                    #s.e value of wi
	interval=[]
	chi2= 0
	selection=['+','-','0']

	chi21=0
	interval1=[]
	dif = 0
	sq = 0
	print '----------------------------------------------------'
	print 'log-likehood Chi-squre test 对数似然卡方检验:  +++++++++++++'
	for i in range(len(Category[j])):
		#对数似然卡方检验
		if(numU[i]==0):
			numU[i]=1
			freU[i]=float(1.0/sumU)
		if(numA[i]==0):
			numA[i]=1
			freA[i]=float(1.0/sumA)
	
		wiTemp =float(freU[i]/freA[i])
		wiList.append(wiTemp)	
		seTemp = wiTemp*float(math.sqrt(1.0/numU[i]-1.0/sumU+1.0/numA[i]-1.0/sumA))  #function use?
	
		seWiList.append(seTemp)
	
		intervalTemp = [wiTemp-Z*seTemp,wiTemp+Z*seTemp]
		interval.append(intervalTemp)
		chi2T = float(numU[i])*math.log(float(numU[i])/( float(numU[i]+numA[i])*sumU/(sumU+sumA)))+float(numA[i])*math.log(float(numA[i])/( float(numU[i]+numA[i])*sumA/(sumU+sumA)))
		chi2+= chi2T*2
		#~ chi2T = float(numU[i])*math.log(float(numU[i])/(numA[i]))
		#~ chi2+= chi2T*2
	
		#selection jugement
		if(intervalTemp[0]>1):
			a = selection[0]
		else:
			if(intervalTemp[1]<1):
				a=selection[1]
			else:
				a=selection[2]	
	
		print 'Category%2d:   Wi:%-9.3f s.e.(Wi):%9.3f   interval:(%9.3f   -- %9.3f)   selection:%4s'  %  (i+1,wiTemp,seTemp,intervalTemp[0],intervalTemp[1],a)
	

	print ''
	print ' chi2:%-20.3f df=%2d  P =%9.5F' % (chi2 ,len(Category[j])-1,1-float(st.chi2.cdf(chi2,len(Category)-1)))
	print ''


	#~ print 'Chi-squre goodness of fit test 拟合优度卡方检验:  ++++++++++++'
	#~ for i in range(len(Category[j])):
		#~ #拟合优度卡方检验的方法
		#~ chi21T = math.pow(float(numU[i]-numA[i]),2)/numA[i]
		#~ chi21 += chi21T
	
		#~ dif = freA[i] - freU[i]
		#~ sq = math.sqrt(freA[i]*(1-freA[i])/numA[i]+freU[i]*(1-freU[i])/numU[i])
		#~ intervalTemp1 = [dif-Z*sq,dif+Z*sq]
		#~ interval1.append(intervalTemp1)
	
		#~ #selection jugement
		#~ if(intervalTemp1[0]>0):
			#~ a = selection[1]
		#~ else:
			#~ if(intervalTemp1[1]<0):
				#~ a=selection[0]
			#~ else:
				#~ a=selection[2]	
		#~ print 'Category%2d:  used:%-6.3f  availiable:%.3f   interval:(%9.3f   -- %9.3f)    selection:%4s '  %  (i+1,freU[i],freA[i],intervalTemp1[0],intervalTemp1[1],a)
		
	#~ #拟合优度卡方检验
	#~ print ''
	#~ print ' chi2:%-20.3f df=%2d  P =%9.5F' % (chi21 ,len(Category[j])-1,1-float(st.chi2.cdf(chi21,len(Category)-1)))
	#~ print ''




