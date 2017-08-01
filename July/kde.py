#!/usr/bin/env python
# -*- coding:utf-8 -*-July23 2017
#Robin
from PIL import Image
from glob import glob
import os
import numpy as np


# import matplotlib.pyplot as plt
# from sklearn.neighbors import KernelDensity
# import read_dataCSV
#
# points = read_dataCSV.readData()#
# print points
#
# kde = KernelDensity(bandwidth=0.04, metric='haversine',
#                     kernel='gaussian', algorithm='ball_tree')
# kde.fit(points)


import numpy as np
from scipy import stats
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# # Generate random data.
# n = 1000
# m1, m2 = np.random.normal(-3., 3., size=n), np.random.normal(-3., 3., size=n)
# # Define limits.
# xmin, xmax = min(m1), max(m1)
# ymin, ymax = min(m2), max(m2)
# ext_range = [xmin, xmax, ymin, ymax]


import read_dataCSV

p = np.array(read_dataCSV.readData())
p *= np.pi / 180.

# Define limits.
xmax, ymax = np.max(p,axis = 0)
xmin, ymin = np.min(p,axis = 0)
ext_range = [xmin, xmax, ymin, ymax]



# Format data.
x, y = np.mgrid[xmin:xmax:100j, ymin:ymax:80j]

positions = np.vstack([x.ravel(), y.ravel()])



# Define some point to evaluate the KDEs.
x1, y1 = 0.5, 0.5
# Bandwidth value.
bw = 0.04


# -------------------------------------------------------
# Perform a kernel density estimate on the data using sklearn.

kernel_sk = KernelDensity(kernel='gaussian', bandwidth=bw).fit(p)
# # log values
# iso2 = np.exp(kernel_sk.score_samples([[x1, y1]]))
# print 'iso2 = ', iso2[0]


# Plot
fig = plt.figure(figsize=(10, 10))




# Sklearn
plt.title("Sklearn", x=0.5, y=0.92, fontsize=10)
# Evaluate kernel in grid positions.
k_pos2 = np.exp(kernel_sk.score_samples(zip(*positions)))



kde2 = np.reshape(k_pos2.T, x.shape)
plt.imshow(np.rot90(kde2), cmap=plt.cm.YlOrBr, extent=ext_range)

plt.contour(x, y, kde2, 5, colors='k', linewidths=0.6)

fig.tight_layout()
#plt.savefig('KDEs', dpi=300, bbox_inches='tight')
plt.show()