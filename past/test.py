import MySQLdb
import math
import csv
import os,sys,time,gdal
import random
import scipy.stats as st

from gdalconst import *

#calculate the result
sumU=6640
numU=[3994,2504,2,140]
freU=[0.602,0.377,0.000,0.021]
numA=[2170,4366,26,41]
freA=[0.329,0.662,0.004,0.006]
sumA=6603


Z=st.norm.ppf(1-0.05/len(numU))
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
print 'log-likehood Chi-squre test   +++++++++++++'
for i in range(4):
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
print ' chi2:%-20.3f df=%2d  P =%9.5F' % (chi2 ,len(numA)-1,1-float(st.chi2.cdf(chi2,len(numA)-1)))
print ''