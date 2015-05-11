#本脚本读取目标鸟类gps记录点，模拟生成同数量记录点，统计目标划分各范围内的数量
import MySQLdb
import math
import csv

birds=['BH07_67582','BH07_67586','BH07_67695','BH07_74902','BH08_82076','BH08_82077','BH08_82078']

xTopLeft = 96.00
yTopLeft = 37.90
xBottomRight = 101.00
yBottomRight = 34.40
dif=0.02



conn = MySQLdb.connect(host='localhost',user = 'root', passwd = '123456')
conn.select_db('gps')

M1=[]
for i in range(len(birds)):
	countNum = [0]*250*175
	sql = "select animal,longitude,latitude,DATE(date_time) as date from gps_bh where animal = %s and latitude >= %s and latitude < %s and longitude >= %s and longitude < %s and date_time BETWEEN '2008-01-01 00:00:00' and '2009-01-01 00:00:00' order by date asc"
	param=[birds[i],yBottomRight,yTopLeft,xTopLeft,xBottomRight]
	cursor = conn.cursor()
	n=cursor.execute(sql,param)
	print "influence rows : "+str(cursor.rowcount)
	for row in cursor.fetchall():
		x = row[1]
		y = row[2]
		subY = int(math.floor((yTopLeft-y)/dif))*250
		subX = int(math.floor((x-xTopLeft)/dif))
		num = subY+subX
		countNum[num] = countNum[num]+1
	M1.append(countNum)	

for i in M1:
	cnt=0
	for j in i:
		if j!=0:
			cnt+=1
	print cnt

#write to csv				
writer = csv.writer(file('M1.csv','wb'))
writer.writerow(birds)
for line in M1:
	writer.writerow(line)


print len(M1)	
print len(M1[1])
print len(M1[5])

		

