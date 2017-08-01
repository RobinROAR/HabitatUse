#本模块按鸟ID与出入时间导出特定地区的鸟类坐标

import MySQLdb
import math
import csv


#定义原始分析区域范围

xTopLeft = 96.00
yTopLeft = 37.90
xBottomRight = 101.00
yBottomRight = 34.40

#上左右下
QHH = [37.625,98.772,101.011,36.255]
LRW = [30.23,90.257,91.79,29.145]
NLRW = [30]


def writeCsv():								
	global List
	
	writer = csv.writer(file('Source/LRWPU.csv','wb'))
	writer.writerow(['x','y'])
	for line in List:
		writer.writerow(line)
		print line

birds07=['BH07_67582','BH07_67695','BH07_74901','BH07_74902']
birds08=['BH08_82079','BH08_82080','BH08_82082','BH08_82084','BH08_82086']

dateQHH07 = [['2007-03-25 00:00:00','2007-07-02 00:00:00'],['2007-03-29 00:00:00','2007-06-22 00:00:00'],['2007-03-31 00:00:00','2007-06-21 00:00:00'],['2007-03-30 00:00:00','2007-10-24 00:00:00']]
dateQHH08 = [['2008-04-02 00:00:00','2008-08-31 00:00:00'],['2008-04-02 00:00:00','2008-06-29 00:00:00'],['2008-03-30 00:00:00','2008-09-29 00:00:00'],['2008-03-30 00:00:00','2008-09-18 00:00:00'],['2008-03-31 00:00:00','2008-08-21 00:00:00']]

dateLRW07 = [['2007-11-13 00:00:00','2008-04-08 00:00:00'],['2007-11-01 00:00:00','2008-04-25 00:00:00'],['2007-11-11 00:00:00','2008-04-06 00:00:00'],['2007-11-17 00:00:00','2008-04-08 00:00:00']]
dateLRW08 = [['2008-11-12 00:00:00','2009-03-24 00:00:00'],['2008-11-02 00:00:00','2009-03-23 00:00:00'],['2008-11-16 00:00:00','2009-04-01 00:00:00'],['2008-11-10 00:00:00','2009-04-06 00:00:00'],['2008-10-29 00:00:00','2009-03-14 00:00:00']]


#实际参数
#~ birds=birds07+birds08
#~ date=dateQHH07+dateQHH08
birds=birds07+birds08
date=dateLRW07+dateLRW08


print len(birds)
print len(date)


conn = MySQLdb.connect(host='localhost',user = 'root', passwd = '123456')
conn.select_db('GPStemp')
List=[]

for i in range(len(birds)):
	
	#ignore same position
	#~ sql = "select animal,longitude,latitude,DATE(date_time) as date from gps_bh where animal = %s and latitude >= %s and latitude < %s and longitude >= %s and longitude < %s and date_time BETWEEN %s and %s  order by date asc "
	#~ param=[birds[i],QHH[3],QHH[0],QHH[1],QHH[2],date[i][0],date[i][1]]
	
	#has region define
	sql = "select animal,longitude,latitude,date_time as date from gps_bh where animal = %s and latitude >= %s and latitude < %s and longitude >= %s and longitude < %s and date_time BETWEEN %s and %s  order by date asc "
	param=[birds[i],LRW[3],LRW[0],LRW[1],LRW[2],date[i][0],date[i][1]]
	
	#~ sql = "select DISTINCT animal,longitude,latitude,date_time as date from gps_bh where animal = %s and date_time BETWEEN %s and %s  order by date asc "
	#~ param=[birds[i],date[i][0],date[i][1]]
	
	cursor = conn.cursor()
	n=cursor.execute(sql,param)
	print "influence rows : "+str(cursor.rowcount)
	for row in cursor.fetchall():
		x = row[1]
		y = row[2]
		z = row[0]
		#~ q = row[3]
		temp=[z,x,y]
		List.append(temp)

writeCsv()
print len(List)
		
