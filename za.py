

import MySQLdb
import math
import csv





def writeCsv():								
	global List
	
	writer = csv.writer(file('Source/zhangao','wb'))
	writer.writerow(['datetime','x','y'])
	for line in List:
		writer.writerow(line)
		print line

birds07=['BH07_67582']
dateQHH07 = [['2007-01-01 00:00:00','2010-01-02 00:00:00']]
birds=birds07
date=dateQHH07

print len(birds)
print len(date)


conn = MySQLdb.connect(host='localhost',user = 'root', passwd = '123456')
conn.select_db('gps')
List=[]

for i in range(len(birds)):
	
	#ignore same
	#~ sql = "select animal,longitude,latitude,DATE(date_time) as date from gps_bh where animal = %s and latitude >= %s and latitude < %s and longitude >= %s and longitude < %s and date_time BETWEEN %s and %s  order by date asc "
	#~ param=[birds[i],QHH[3],QHH[0],QHH[1],QHH[2],date[i][0],date[i][1]]
	
	sql = "select animal,longitude,latitude,date_time from gps_bh where animal = %s  and date_time BETWEEN %s and %s  order by date asc "
	param=[birds[i],date[i][0],date[i][1]]
	
	cursor = conn.cursor()
	n=cursor.execute(sql,param)
	print "influence rows : "+str(cursor.rowcount)
	for row in cursor.fetchall():
		z = row[3]
		x = row[1]
		y = row[2]
		
		temp=[z,x,y]
		List.append(temp)

writeCsv()
print len(List)
		
