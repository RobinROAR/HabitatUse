import numpy as np
import csv  


M1 = np.matrix([])
M2 = np.matrix([])

def readM2(filename):
	global M2
	csvFile = file(filename,'rb')
	reader = csv.reader(csvFile)
	temp=[]
	for line in reader:
		lineT = []
		if reader.line_num == 1:
			continue
		#covert to float from string
		for cell in line:
			y = float(cell)
			lineT.append(y)
		temp.append(lineT)
	#user array to store list
	b = np.array(temp)
	a = np.matrix(b)
	#take the mean of each col
	means = a.mean(axis = 0)
	stds = a.std(axis = 0)
	
	M2 = (a-means)/stds

def readM1(filename):
	global M1
	csvFile = file(filename,'rb')
	reader = csv.reader(csvFile)
	temp=[]
	for line in reader:
		lineT = []
		if reader.line_num == 1:
			continue
		#covert to float from string
		for cell in line:
			y = float(cell)
			lineT.append(y)
		temp.append(lineT)
	#user array to store list
	b = np.array(temp)
	a = np.matrix(b)
	#take the sum of each col
	sum = a.sum(axis = 1)	
	M1 = a/sum

readM2('M2.csv')
readM1('M1.csv')

print M1.shape
print M2.shape

M3=np.dot(M1,M2)


#print M3

data = M3
#计算协防差矩阵
#~ covariance = np.transpose(data)*data/5
#~ eigenvalues,eigenvectors = np.linalg.eig(covariance)
#~ feature_vectors = np.transpose(eigenvectors)

#~ final_data = feature_vectors*np.transpose(data)

#~ print feature_vectors
#print final_data

topNfeat = 3
covMat = np.cov(data,rowvar=0)
#sort eigVals
eigVals,eigVects = np.linalg.eig(np.mat(covMat))

print eigVals
eigValInd = np.argsort(eigVals)

print eigValInd

eigValInd = eigValInd[:-(topNfeat+1):-1]

print eigValInd

redEigVects = eigVects[:,eigValInd]

print redEigVects










