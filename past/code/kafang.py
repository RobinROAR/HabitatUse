import MySQLdb
import math
import csv
import os,sys,time,gdal
import random
import scipy.stats as st

from gdalconst import *

Birds=['BH07_67582','BH07_67586','BH07_67695','BH07_74902']
Category=[[1,2000],[2000,4000],[4000,6000],[6000,99999000]]
#DateNum use to  store  Birds' records num 
dataNum = []
#countNum use to store every categories' num
countNum = [0]*len(Category)
RcountNum=[0]*len(Category)

xTopLeft = 96.00
yTopLeft = 37.90
xBottomRight = 101.00
yBottomRight = 34.40
tif = 'water1.tif'

#connect to database 
conn = MySQLdb.connect(host='localhost',user = 'root', passwd = '123456')
conn.select_db('gps')
gdal.AllRegister()


#random  
def getRandom(n):
	randoms=[]
	for i in range(n):
		x = random.uniform(xTopLeft,xBottomRight)
		y = random.uniform(yBottomRight,yTopLeft)
		randoms.append([x,y])
	return randoms
		
		

for i in range(len(Birds)):
	#read coordinates by birds
	sql = "select animal,longitude,latitude,DATE(date_time) as date from gps_bh where animal = %s and latitude >= %s and latitude < %s and longitude >= %s and longitude < %s and date_time BETWEEN '2008-01-01 00:00:00' and '2009-01-01 00:00:00' order by date asc"
	param=[Birds[i],yBottomRight,yTopLeft,xTopLeft,xBottomRight]
	cursor = conn.cursor()
	n=cursor.execute(sql,param)
	dataNum.append(cursor.rowcount)
	print Birds[i]+":    "+str(cursor.rowcount)	
	
	randomList = getRandom(cursor.rowcount)
	
	listT = []
	for row in cursor.fetchall():
		x = row[1]
		y = row[2]
		listT.append([row[1],row[2]])
	
	#get raster's info
	ds = gdal.Open(tif,GA_ReadOnly)
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
print '---------------------我是华丽的分割线-------------------------------'
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

print '---------------------我是华丽的分割线-------------------------------'

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

Z=st.norm.ppf(1-0.05/(2*len(Category)))

wiList=[]                                       #value of   ui/ai
seWiList=[]                                    #s.e value of wi
interval=[]
chi2= 0

chi21=0
interval1=[]
dif = 0
sq = 0

print 'log-likehood Chi-squre test 对数似然卡方检验:  ++++++++++++=+'
for i in range(len(Category)):
	#对数似然卡方检验
	wiTemp =float(freU[i]/freA[i])
	wiList.append(wiTemp)	
	
	seTemp =float(math.sqrt(1.0/numU[i]-1.0/sumU+1.0/numA[i]-1.0/sumA))  #function use?
	seWiList.append(seTemp)
	
	intervalTemp = [wiTemp-Z*seTemp,wiTemp+Z*seTemp]
	interval.append(intervalTemp)
	
	chi2T = float(numU[i])*math.log(float(numU[i])/(numU[i]*freU[i]*freU[i]))+float(numA[i])*math.log(float(numA[i])/(numA[i]*freA[i]*freA[i]))
	chi2+= chi2T*2
	
	print 'Category%2d:   Wi:%-9.3f s.e.(Wi):%9.3f   interval:%9.3f %9.3f '  %  (i+1,seTemp,seTemp,intervalTemp[0],intervalTemp[1])
	

print ''
print ' chi2:%-20.3f df=%2d  P =%9.5F' % (chi2 ,len(Category)-1,1-float(st.chi2.cdf(chi2,len(Category)-1)))

print 'Chi-squre goodness of fit test 拟合优度卡方检验:  ++++++++++++=+'
for i in range(len(Category)):
	#拟合优度卡方检验的方法
	chi21T = float(numU[i]-numA[i])/numA[i]
	chi21 += chi21T
	
	dif = freA[i] - freU[i]
	sq = math.sqrt(freA[i]*(1-freA[i])/numA[i]+freU[i]*(1-freU[i])/numU[i])
	intervalTemp1 = [dif-Z*sq,dif+Z*sq]
	interval1.append(intervalTemp1)
	
	print 'Category%2d:  used:%-6.3f  availiable:%.3f   interval:%9.3f %9.3f '  %  (i+1,freU[i],freA[i],intervalTemp1[0],intervalTemp1[1])
	#print WiTemp,seTemp

#拟合优度卡方检验
print ''
print ' chi2:%-20.3f df=%2d  P =%9.5F' % (chi21 ,len(Category)-1,1-float(st.chi2.cdf(chi21,len(Category)-1)))





