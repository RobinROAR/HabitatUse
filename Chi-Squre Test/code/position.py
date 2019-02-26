import csv

xTopLeft = 96.00
yTopLeft = 37.90
xBottomRight = 101.00
yBottomRight = 34.40
allPos=[]
dif = 0.02

def writePosCsv():
	global allPos
	writer = csv.writer(file('pos.csv','wb'))
	writer.writerow(['Xposition','Yposition'])
	for line in allPos:
		writer.writerow(line[2])

numX = int(abs(xBottomRight - xTopLeft) / dif)
numY = int(abs(yBottomRight - yTopLeft) / dif)

y = round(yTopLeft,3)
for i in range(numY):
	x = round(xTopLeft,2)	
	for j in range(numX):
		
		posTemp = [[x,y]]
		x=round((x+dif),2)
	
		posTemp.append([x,y])
		midx = round((x-dif/2),2)
		midy = round((y+dif/2),2)
		
		posTemp.append([midx,midy])
		allPos.append(posTemp)
		#print posTemp
	y=round((y-dif),3)

print len(allPos)
writePosCsv()

