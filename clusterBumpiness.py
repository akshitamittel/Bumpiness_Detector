import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os
import sys
import collections


## Get user inputs and check if they are entered correctly
parser = argparse.ArgumentParser()
parser.add_argument("--MBHx", default="MBHxAggFeatures.npy")
parser.add_argument("--MBHy", default="MBHyAggFeatures.npy")
parser.add_argument("--labelFile", default="labels.npy")
parser.add_argument("--clusterFile", default="clusters.npy")
parser.add_argument("--environ", default="test")
args = parser.parse_args()

x_data = np.load(args.MBHx)
y_data = np.load(args.MBHy)
bach = 3

def f(x, num, den):
	return x * 1.0 * num / den

f = np.vectorize(f)

def loadData(x_data, y_data):
	'''
	Load the data and delete the last and first element.
	These elements are always 0 and cause errors in clustering.
	Label these clusters as -1.
	'''
	x = x_data
	y = y_data
	x_data = np.delete(x_data,0,0)
	x_data = np.delete(x_data,len(x_data)-1,0)
	y_data = np.delete(y_data,0,0)
	y_data = np.delete(y_data,len(y_data)-1,0)
	X = np.asarray([x_data.tolist(), y_data.tolist()])
	X = np.swapaxes(X,0,1)
	return X, x, y

def kMeans(X, i):
	'''
	Perform k-means clustering on the features (MBHx/MBHy)
	Return the labels and cluster centres.
	'''
	kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
	labels = list(kmeans.labels_)
	clusters = list(kmeans.cluster_centers_)
	labels.insert(0, -1)
	labels.append(-1)
	X = np.vstack((np.asarray([0,0]),X))
	X = np.vstack((X,np.asarray([0,0])))
	print labels
	print len(labels)
	return clusters, labels, X

def plot_kMeans(X,labels):
	'''
	Plot the clusters for visual inspection.
	'''
	for (idx,i) in enumerate(X):
		if labels[idx] == 0:
			# print str(idx) + " :0 Here"
			plt.scatter(i[0],i[1],c='r',marker='o')
		elif labels[idx] == 1:
			# print str(idx) + " :1 Here"
			plt.scatter(i[0],i[1],c='b',marker='o')
		elif labels[idx] == 2:
			# print str(idx) + " :2 Here"
			plt.scatter(i[0],i[1],c='g',marker='o')
	# plt.show()


def smoothen(elem, idx, arr, rng):
	'''
	Smoothen the ranges which have turns. 
	'''
	start = idx - rng
	if start < 0:
		start = 0
	end = idx + rng
	arr1 = arr[start:end]
	return sum(arr1)*1.0/len(arr1)

def smoothenPlot(x, y, labels):
	'''
	Smoothen the plot based on the classes that the points are labelled as.
	Classes: 
	1. Bump/Disturbance
	2. Minor Disturbance
	3. Turn/Disturbance
	'''
	x_data = []
	y_data = []
	for (idx,i) in enumerate(labels):
		if i == 1:
			x_data.append(smoothen(x[idx],idx,x,3))
			y_data.append(smoothen(y[idx],idx,y,3))
		elif i == 2: 
			x_data.append(smoothen(x[idx],idx,x,2))
			y_data.append(smoothen(y[idx],idx,y,2))
		else:
			x_data.append(x[idx])
			y_data.append(y[idx])
	return x_data, y_data

def plot_Bumpiness(x,y):
	'''
	Plit the values of MBHx and MBHy for visual inspection.
	'''
	plt.clf()
	x = np.asarray(x)
	y = np.asarray(y)
	x_axis = range(len(x))
	plt.plot(x_axis,x)
	plt.plot(x_axis,y)
	plt.axis([0, 60, 0, 10])
	# plt.show()

if args.environ == "dep":
	'''
	Reiterate the smoothening and clustering process to get a better estimate of bumpiness during turns.
	'''
	for i in range(bach):
		X, MBHx, MBHy = loadData(x_data,y_data)
		print ("kMeans", i)
		clusters, labels, X = kMeans(X,i)
		# This saves the labels and cluster centres for the initial iteration.
		# The non-smoothed labels are used to display and catergorise situations in the demo Video.
		if i == 0:
			np.save(args.labelFile, labels)
			np.save(args.clusterFile, clusters)
			print ("cluster centres", clusters)
		plot_kMeans(X,labels)
		print("smoothen", i)
		x, y = smoothenPlot(MBHx.tolist(), MBHy.tolist(), labels)
		x_data = np.asarray(x)
		y_data = np.asarray(y)
		plot_Bumpiness(x,y)