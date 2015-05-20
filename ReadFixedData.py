#encoding = utf-8
import csv
import MySQLdb
		
#read CSV
def readFromCsv(filename):
	
	all_pos=[]
	csvFile=file(filename,'rb')
	reader=csv.reader(csvFile)
	for line in reader:
		if reader.line_num == 1:  
			continue  		
		pos = [line[0],line[1],line[2],line[3]]                             
		all_pos.append(pos)
			
	print('all_pos:'+str(len(all_pos)))
	return all_pos

conn = MySQLdb.connect(host='localhost',user = 'root', passwd = '123456')
conn.select_db('GPStemp')
cursor = conn.cursor()

# 从ｃｓｖ读取数据
result = readFromCsv('birdDataLG.csv')
cnt = 0
#~ #写入数据库
for i in result:
    sql = 'insert into gps_bh(animal,longitude,latitude,date_time) values(%s,%s,%s,%s)'
    param = (i[0],i[1],i[2],i[3])
    n =cursor.execute(sql,param)
    cnt+=n

conn.commit()


print '存储完毕'
#查询插入情况
sql = 'select * from gps_bh'
n =cursor.execute(sql)
for row in cursor.fetchall():
	print row

	
cursor.close()
conn.close()


	
	